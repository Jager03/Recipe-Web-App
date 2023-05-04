from django import forms
from django.forms import ModelForm
from .models import Receta, Ingrediente

class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ('nombre', 'preparacion', 'foto')

class IngredienteForm(ModelForm):
    class Meta:
        model = Ingrediente
        fields = ("__all__")

