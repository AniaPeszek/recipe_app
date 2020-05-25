from django.urls import path

from . import views

urlpatterns = [
    path('<int:recipe_id>', views.recipe, name='recipe'),
    path('', views.index, name='recipes'),
    path('search', views.search, name='search'),
    path('add_to_favourites', views.add_to_favourites, name='add_to_favourites'),
    path('remove_from_favourites', views.remove_from_favourites, name='remove_from_favourites')
]