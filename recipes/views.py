from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Recipe
from django.contrib.auth.models import User


def index(request):
    recipes = Recipe.objects.order_by('-added_date').filter(is_published=True)
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page')
    page_recipes = paginator.get_page(page)

    context = {'recipes': page_recipes}

    return render(request, 'recipes/recipes.html', context)


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    is_favourite = False

    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        if user in recipe.users_who_like.all():
            is_favourite = True

    context = {'recipe': recipe, 'is_favourite': is_favourite}
    return render(request, 'recipes/recipe.html', context)


def add_to_favourites(request):
    if request.method == "POST":
        try:
            recipe_id = request.POST.get('recipe_id')
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            user = get_object_or_404(User, pk=request.user.id)
            if not user in recipe.users_who_like.all():
                recipe.users_who_like.add(user)
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def remove_from_favourites(request):
    if request.method == "POST":
        try:
            recipe_id = request.POST.get('recipe_id')
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            user = get_object_or_404(User, pk=request.user.id)
            if user in recipe.users_who_like.all():
                recipe.users_who_like.remove(user)
                print('usunięto')
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


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
