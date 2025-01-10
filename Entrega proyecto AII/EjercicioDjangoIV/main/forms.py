#encoding:utf-8
from django import forms
from main.models import RopaHombre

from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
   

class BusquedaRopaForm(forms.Form):
    query = forms.CharField(label='Buscar por nombre', max_length=255)