#encoding:utf-8
from django import forms
from main.models import Producto

from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
   
"""
class VinosPorAnyo(forms.Form):
    anyo = forms.IntegerField(label="Introduzca un año (entre 1000 y el año actual) ", widget=forms.TextInput, validators=[MinValueValidator(1000), MaxValueValidator(datetime.today().year)], required=True)
    
class VinosPorUvas(forms.Form):
    uva = forms.ModelChoiceField(label="Seleccione un tipo de uva ", queryset=Uva.objects.all())
"""