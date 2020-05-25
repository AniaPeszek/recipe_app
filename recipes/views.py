from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Recipe


def index(request):
    recipes = Recipe.objects.order_by('-added_date').filter(is_published=True)
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page')
    page_recipes = paginator.get_page(page)

    context = {'recipes': page_recipes}

    return render(request, 'recipes/recipes.html', context)


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipes/recipe.html', context)


def search(request):
    queryset_list = Recipe.objects.order_by('-added_date')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(Q(description__icontains=keywords) | Q(title__icontains=keywords))

    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            queryset_list = queryset_list.filter(category=category)

    if 'diet' in request.GET:
        diet = request.GET['diet']
        if diet:
            queryset_list = queryset_list.filter(diet__lte=diet)

    if 'difficulty' in request.GET:
        difficulty = request.GET['difficulty']
        if difficulty:
            queryset_list = queryset_list.filter(difficulty=difficulty)

    category_choices = {v.value: v.label for k, v in Recipe.CategoryChoices}
    diet_choices = {v.value: v.label for k, v in Recipe.DietChoices}
    difficulty_choices = {v.value: v.label for k, v in Recipe.DifficultyChoices}

    paginator = Paginator(queryset_list, 6)
    page = request.GET.get('page')

    try:
        page_recipes = paginator.page(page)
    except PageNotAnInteger:
        page_recipes = paginator.page(1)
    except EmptyPage:
        page_recipes = paginator.page(paginator.num_pages)

    context = {'category_choices': category_choices,
               'diet_choices': diet_choices,
               'difficulty_choices': difficulty_choices,
               'recipes': page_recipes,
               'values': request.GET
               }

    return render(request, 'recipes/search.html', context)
