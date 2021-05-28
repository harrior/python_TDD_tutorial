from django.db import models
# Create your models here.


class List(models.Model):
    """список"""
    pass


class Item(models.Model):
    """Элемент"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

