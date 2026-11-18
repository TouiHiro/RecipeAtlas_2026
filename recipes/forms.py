from django import forms
from .models import Recipe, Process, Tag, Ingredients
from django.forms import inlineformset_factory


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

        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
            'recipe_title' : forms.TextInput(attrs={
                'name' : 'recipe_title',
                'required': True
                }),
            'recipe_detail' : forms.Textarea(attrs={
                'id' : 'detail',
                'name' : 'recipe_detail'
            }),
            
            'recipe_img': forms.FileInput(attrs={
                'id': 'file_input',
                'name': 'recipe_img'
            })
        }


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = [
            'process_num',
            'process_detail',
            'process_img'
        ]


RecipeProcessFormSet = inlineformset_factory(
    Recipe,
    Process,
    form=ProcessForm,
    extra=3,
    can_delete=True
)
