from django.conf import settings
from django.db import models
from django.utils import timezone
from django_utils.choices import Choice, Choices
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


class Recipe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    users_who_like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='favourites')
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    description = models.TextField()
    preparation_time_in_minutes = models.IntegerField()
    serves = models.IntegerField(blank=True)

    class CategoryChoices(Choices):
        dinner = Choice(1, 'Obiady')
        breakfast = Choice(2, 'Śniadania')
        supper = Choice(3, 'Kolacje')
        snack = Choice(4, 'Przekąski')
        dessert = Choice(5, 'Desery')
        other = Choice(6, 'Inne')

    category = models.PositiveIntegerField(choices=CategoryChoices.choices, default=CategoryChoices.dinner)

    class DifficultyChoices(Choices):
        easy = Choice(1, 'Łatwe')
        medium = Choice(2, 'Średnie')
        hard = Choice(3, 'Trudne')

    difficulty = models.PositiveIntegerField(choices=DifficultyChoices, default=DifficultyChoices.easy)

    class DietChoices(Choices):
        vegan = Choice(1, 'Wegańska')
        vegetarian = Choice(2, 'Wegetariańska')
        meat = Choice(3, 'Bez ograniczeń')

    diet = models.PositiveIntegerField(choices=DietChoices, default=DietChoices.meat)
    ratings = GenericRelation(Rating, related_query_name='recipes_rating')
    is_published = models.BooleanField(default=True)
    is_recipe_of_month = models.BooleanField(default=False)
    added_date = models.DateTimeField(default=timezone.now)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title
