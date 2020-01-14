from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms


class PlayerForm(forms.ModelForm):
    suggested_number = forms.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
     )


class GameForm(models.ModelForm):
    guessed_number = forms.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
