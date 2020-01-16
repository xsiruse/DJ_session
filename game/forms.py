from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from game.models import *


class GameFormPost(forms.ModelForm):
    guessed_number = forms.IntegerField(
        label="Введите число",
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        model = Game
        fields = ('guessed_number',)
