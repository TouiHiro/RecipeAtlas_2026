from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm
from django.views import View
# Create your views here.
def my_view(request):
    return render(request, 'recipe_insert.html')