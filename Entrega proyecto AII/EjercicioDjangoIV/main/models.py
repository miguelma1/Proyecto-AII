#encoding:utf-8
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    enlace = models.URLField()
    precio = models.CharField(max_length=100)
    precio_original = models.CharField(max_length=100, blank=True, null=True)
    descuento = models.CharField(max_length=100, blank=True, null=True)
    tallas = models.TextField()

    def __str__(self):
        return self.nombre

"""
class Pais(models.Model):
    idPais = models.IntegerField(primary_key=True)
    nombre = models.TextField(verbose_name='Pais', unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
        
class Denominacion(models.Model):
    idDenominacion = models.IntegerField(primary_key=True)
    nombre = models.TextField(verbose_name='Denominacion')
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )

class Uva(models.Model):
    idUva = models.IntegerField(primary_key=True)
    nombre = models.TextField()

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering =('nombre', )
                
class Vino(models.Model):
    idVino = models.IntegerField(primary_key=True)
    nombre = models.TextField()
    precio = models.FloatField()
    denominacion = models.ForeignKey(Denominacion, on_delete=models.SET_NULL, null=True)
    uvas = models.ManyToManyField(Uva)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
"""

