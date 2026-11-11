from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        # モデルのカラムと同じ名前で
        fields = [
            'user',
            'recipe_title',
            'recipe_img',
            'recipe_detail',
            'region',
            'tag'
        ]