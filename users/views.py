from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ta nazwa użytkownika jest już zajęta.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Ten email jest już zajęty.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Zostałeś zarejestrowany w Kuku! Możesz się zalogować.')
                    return redirect('login')
        else:
            messages.error(request, "Hasło muszą być takie same")
            return redirect('register')
    else:
        return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Zalogowano")
            return redirect('dashboard')
        else:
            messages.error(request, 'Nieprawidłowy login lub hasło')
            return redirect('login')
    else:
        return render(request, 'users/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "Zostałeś wylogowany")
        return redirect('index')


@login_required()
def dashboard(request):
    recipes = request.user.favourites.order_by('-added_date').all()
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page')
    try:
        page_recipes = paginator.page(page)
    except PageNotAnInteger:
        page_recipes = paginator.page(1)
    except EmptyPage:
        page_recipes = paginator.page(paginator.num_pages)

    context = {'recipes': page_recipes}

    return render(request, 'users/dashboard.html', context)


@login_required()
def user_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-added_date').all()
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page')
    try:
        page_recipes = paginator.page(page)
    except PageNotAnInteger:
        page_recipes = paginator.page(1)
    except EmptyPage:
        page_recipes = paginator.page(paginator.num_pages)

    context = {'recipes': page_recipes}

    return render(request, 'users/user_recipes.html', context)
