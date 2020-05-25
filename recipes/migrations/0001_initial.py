# Generated by Django 3.0.6 on 2020-05-22 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_utils.choices


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('ingredients', models.TextField()),
                ('description', models.TextField()),
                ('preparation_time_in_minutes', models.IntegerField()),
                ('serves', models.IntegerField(blank=True)),
                ('category', models.PositiveIntegerField(choices=[(1, django_utils.choices.Choice(1, 'Obiady')), (2, django_utils.choices.Choice(2, 'Śniadania')), (3, django_utils.choices.Choice(3, 'Kolacje')), (4, django_utils.choices.Choice(4, 'Przekąski')), (5, django_utils.choices.Choice(5, 'Desery')), (6, django_utils.choices.Choice(6, 'Inne'))], default=1)),
                ('difficulty', models.PositiveIntegerField(choices=[(1, django_utils.choices.Choice(1, 'Łatwe')), (2, django_utils.choices.Choice(2, 'Średnie')), (3, django_utils.choices.Choice(3, 'Trudne'))], default=1)),
                ('diet', models.PositiveIntegerField(choices=[(1, django_utils.choices.Choice(1, 'Wegańska')), (2, django_utils.choices.Choice(2, 'Wegetariańska')), (3, django_utils.choices.Choice(3, 'Mięsna'))], default=3)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('number_of_ratings', models.IntegerField(default=0)),
                ('is_published', models.BooleanField(default=True)),
                ('is_recipe_of_month', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('photo_main', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('photo_1', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_2', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_3', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('users_who_like', models.ManyToManyField(blank=True, related_name='favourites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
