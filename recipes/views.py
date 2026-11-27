from itertools import zip_longest
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RecipeForm
from .models import Ingredients, Map, Process, Recipe, RecipeIngredient, Tag, User


@transaction.atomic
def recipe_form(request):
    regions = Map.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        title = (request.POST.get("recipe_title") or "").strip()
        detail = (request.POST.get("recipe_detail") or "").strip()
        recipe_img = request.FILES.get("recipe_img")
        region_id = request.POST.get("region")
        region_instance = (
            get_object_or_404(Map, pk=region_id) if region_id else None
        )
        tag_ids = request.POST.getlist("tag")

        ingredient_ids = request.POST.getlist("ingredient_id[]")
        ingredient_names = request.POST.getlist("ingredient_name[]")
        weights = request.POST.getlist("weight[]")

        valid_ingredients = []

        # 1. 食材のチェックだけを行う（ここでは Recipe を作らない）
        for ing_id, name, weight in zip_longest(
            ingredient_ids, ingredient_names, weights, fillvalue=""
        ):
            clean_name = (name or "").strip()
            clean_weight = (weight or "").strip()

            if not clean_name and not clean_weight:
                continue

            if not clean_name or not clean_weight:
                messages.error(request, "食材名と分量の両方を入力してください。")
                return render(
                    request,
                    "recipes/recipe_insert.html",
                    {
                        "form": RecipeForm(request.POST, request.FILES),
                        "regions": regions,
                        "tags": tags,
                    },
                )

            ingredient_instance = None
            if ing_id:
                ingredient_instance = Ingredients.objects.filter(
                    pk=ing_id).first()
            if not ingredient_instance:
                ingredient_instance = Ingredients.objects.filter(
                    name=clean_name).first()

            if not ingredient_instance:
                messages.error(
                    request,
                    f"「{clean_name}」は登録されていない食材です。候補から選択してください。",
                )
                return render(
                    request,
                    "recipes/recipe_insert.html",
                    {
                        "form": RecipeForm(request.POST, request.FILES),
                        "regions": regions,
                        "tags": tags,
                    },
                )

            try:
                weight_val = float(clean_weight)
            except ValueError:
                messages.error(request, "分量は数値で入力してください。")
                return render(
                    request,
                    "recipes/recipe_insert.html",
                    {
                        "form": RecipeForm(request.POST, request.FILES),
                        "regions": regions,
                        "tags": tags,
                    },
                )

            valid_ingredients.append((ingredient_instance, weight_val))

        # 2. 全食材チェックを通過してから Recipe を 1 回だけ作成
        test_user = User.objects.first()
        test_region = Map.objects.first()

        recipe = Recipe.objects.create(
            user=test_user,
            recipe_title=title,
            recipe_detail=detail,
            recipe_img=recipe_img,
            region=region_instance or test_region,
        )

        if tag_ids:
            recipe.tag.set(tag_ids)

        # 3. 検証済みの食材を RecipeIngredient に保存
        for ingredient_instance, weight_val in valid_ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                Ingredient=ingredient_instance,
                weight=weight_val,
            )

        # 4. Process の保存
        process_nums = request.POST.getlist("process_num[]")
        process_details = request.POST.getlist("process_detail[]")

        for num, detail_text in zip(process_nums, process_details):
            if num and detail_text:
                try:
                    process_num = int(num)
                except ValueError:
                    continue

                img = request.FILES.get(f"process_img_{process_num}")
                Process.objects.create(
                    recipe=recipe,
                    process_num=process_num,
                    process_detail=detail_text.strip(),
                    process_img=img,
                )

        return redirect("recipe:recipe_insert")

    form = RecipeForm()
    return render(
        request,
        "recipes/recipe_insert.html",
        {"form": form, "regions": regions, "tags": tags},
    )


def search_ingredients(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        ingredients = Ingredients.objects.filter(name__icontains=query)[:10]
        results = [{"id": ing.id, "name": ing.name} for ing in ingredients]

    return JsonResponse({"results": results})

