from django.db import transaction
from rest_framework import serializers

from .models import Menu, MenuItem, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'opening_time', 'closing_time']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price']


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'title', 'items']

    @transaction.atomic
    def create(self, validated_data: dict) -> Menu:
        items_data = validated_data.pop('items', [])
        menu = Menu.objects.create(**validated_data)
        MenuItem.objects.bulk_create([MenuItem(menu=menu, **item) for item in items_data])
        return menu
