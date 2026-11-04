from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm
from django.views import View
# Create your views here.

def recipe_form(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        # is_valid() で必須項目が入力されているかチェック
        if form.is_valid():
            # save()でdbに保存
            form.save()
            
            return redirect('recipes:index')
    else:
        form = RecipeForm()
    
    recipes = Recipe.objects.all()
    context = {
        'form':form,
        'recipes':recipes
    }
    
    return render(request, 'recipes/index.html', context)

class RecipeDetailView(View):
    # 引数(self, リクエスト, パラメータ)
    def get(self, request, id):
        # Recipeテーブルのrecipe_idがidと一致しているか
        page = get_object_or_404(Recipe, recipe_id=id)
        return render(request, "recipes/detail.html", {"page":page})

class RecipeUpdateView(View):
    def get(self, request, id):
        page = get_object_or_404(Recipe, recipe_id=id)
        form = RecipeForm(instance=page)
        return render(request, "recipes/recipe_update.html", {"form":form})
    
    def post(self, request, id):
        page = get_object_or_404(Recipe, recipe_id=id)
        form = RecipeForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect("recipes:recipe_detail", id=id)
        return render(request, "recipes/recipe_update.html", {"form":form})
recipe_detail = RecipeDetailView.as_view()
recipe_update = RecipeUpdateView.as_view()