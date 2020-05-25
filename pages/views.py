from django.shortcuts import render
from django.http import HttpResponse

from recipes.models import Recipe


def index(request):
    latest_recipes = Recipe.objects.order_by('-added_date').filter(is_published=True)[:3]

    category_choices = {v.value: v.label for k, v in Recipe.CategoryChoices}
    diet_choices = {v.value: v.label for k, v in Recipe.DietChoices}
    difficulty_choices = {v.value: v.label for k, v in Recipe.DifficultyChoices}

    context = {'recipes': latest_recipes,
               'category_choices': category_choices,
               'diet_choices': diet_choices,
               'difficulty_choices': difficulty_choices,
               }
    return render(request, 'pages/index.html', context)


def about(request):
    recipe_of_the_month = Recipe.objects.all().filter(is_recipe_of_month=True).first()
    if not recipe_of_the_month:
        recipe_of_the_month = Recipe.objects.first()
    context = {'recipe': recipe_of_the_month}
    return render(request, 'pages/about.html', context)
