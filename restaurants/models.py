from django.db import models


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=200)

class Menu(models.Model):
    restaurant_id = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    title = models.CharField(max_length=100)

