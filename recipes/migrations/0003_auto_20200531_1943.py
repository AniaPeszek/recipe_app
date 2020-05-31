# Generated by Django 3.0.6 on 2020-05-31 19:43

from django.db import migrations, models
import django_utils.choices


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20200525_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='diet',
            field=models.PositiveIntegerField(choices=[(1, django_utils.choices.Choice(1, 'Wegańska')), (2, django_utils.choices.Choice(2, 'Wegetariańska')), (3, django_utils.choices.Choice(3, 'Bez ograniczeń'))], default=3),
        ),
    ]