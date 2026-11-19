from django.contrib import admin
from .models import Restaurant, Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_time', 'closing_time')
    search_fields = ('name',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'restaurant', 'date')
    list_filter = ('date', 'restaurant')
    search_fields = ('title', 'restaurant__name')
    inlines = [MenuItemInline]
