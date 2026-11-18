from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Ingredients, Map, Process, RecipeIngredient, Tag,User
from .forms import RecipeForm
from django.views import View
from django.db import transaction
from django.http import JsonResponse

# Create your views here.
@transaction.atomic
def recipe_form(request):
    if request.method == "POST":
        title = request.POST.get("recipe_title")
        detail = request.POST.get("recipe_detail")
        recipe_img = request.FILES.get("recipe_img")
        region_id = request.POST.get("region")
        region_instance = get_object_or_404(Map, pk=region_id) if region_id else None;
        
        tag_ids = request.POST.getlist("tag")
        # 仮として登録されているユーザの１番目を取得
        test_user = User.objects.first()
        test_region = Map.objects.first()
        
        recipe = Recipe.objects.create(
            # user=request.user,  # ログイン中のユーザー
            user=test_user,
            recipe_title=title,
            recipe_detail=detail,
            recipe_img=recipe_img,
            # region=region_instance,
            region=test_region
        )

        if tag_ids:
            recipe.tag.set(tag_ids)
        ingredient_names = request.POST.getlist("ingredient_name[]")
        weights = request.POST.getlist("weight[]")

        for name, weight in zip(ingredient_names, weights):
            if name and weight:
                clean_name = name.strip()
                ingredient_instance, created = Ingredients.objects.get_or_create(
                    name=clean_name
                )
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    Ingredient=ingredient_instance,
                    weight=float(weight),
                )

        process_nums = request.POST.getlist("process_num[]")
        process_details = request.POST.getlist("process_detail[]")
        process_imgs = request.FILES.getlist("process_img[]")
        
        for i,(num , detail_text) in enumerate(zip(process_nums, process_details)):
            if num and detail_text:
                img = process_imgs[i] if i < len(process_imgs) else None
                
                Process.objects.create(
                    recipe = recipe,
                    process_num = int(num),
                    process_detail = detail_text,
                    process_img = img
                )
        
        return redirect("recipe:recipe_insert")
    form = RecipeForm()
    regions = Map.objects.all()
    tags = Tag.objects.all()
    context = {
        "form" : form,
        "regions": regions,
        "tags":tags
    }
    return render(request, 'recipes/recipe_insert.html', context)

# from django.http import JsonResponse


# ▼ このビューを追加する
# def search_ingredients_api(request):
#     query = request.GET.get("q", "")
#     results = []
#     if query:
#         # 部分一致で最大10件取得
#         ingredients = Ingredients.objects.filter(name__icontains=query)[:10]
#         results = [{"id": ing.id, "name": ing.name} for ing in ingredients]

#     return JsonResponse({"results": results})

def search_ingredients(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        ingredients = Ingredients.objects.filter(name__icontains=query)[:10]
        results = [{"id":ing.id, "name":ing.name} for ing in ingredients]
    
    return JsonResponse({"results":results})