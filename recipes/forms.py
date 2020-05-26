from django.forms import ModelForm, HiddenInput
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'preparation_time_in_minutes', 'serves', 'difficulty', 'category', 'diet', 'ingredients',
                  'description', 'photo_main', 'photo_1', 'photo_2', 'photo_3']
        labels = {
            'title': 'Tytuł',
            'preparation_time_in_minutes': 'Czas przygotowania w minutach',
            'serves': 'Ilość porcji',
            'difficulty': 'Stopień trudności',
            'category': 'Kategoria',
            'diet': 'Dieta',
            'ingredients': 'Składniki',
            'description': 'Opis przygotowania',
            'photo_main': 'Zdjęcie główne',
            'photo_1': 'Zdjęcie 2',
            'photo_2': 'Zdjęcie 3',
            'photo_3': 'Zdjęcie 4',
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
