from django.contrib import admin

from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    # list_display = ('id', 'title', 'author', 'is_published', 'category', 'diet', 'rating')
    list_display = ('id', 'title', 'author', 'is_published', 'category', 'diet')
    list_display_links = ('id', 'title')
    list_filter = ('category', 'diet', 'author', 'is_recipe_of_month')
    list_editable = ('is_published',)
    search_fields = ('title', 'author', 'category', 'diet', 'ingredients')
    list_per_page = 20


admin.site.register(Recipe, RecipeAdmin)
