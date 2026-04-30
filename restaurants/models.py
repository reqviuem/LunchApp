from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    opening_hours = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    date = models.DateField()
    title = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'date'], name='unique_menu_per_day')
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"
