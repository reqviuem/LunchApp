from django.core.validators import MinValueValidator
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    date = models.DateField()
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ['-date', 'restaurant__name']
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'date'], name='unique_menu_per_day')
        ]
        indexes = [
            models.Index(fields=['date'], name='menu_date_idx')
        ]

    def __str__(self) -> str:
        return f"{self.restaurant.name} - {self.date}"


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f"{self.name} ({self.price})"
