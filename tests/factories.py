from datetime import time
from decimal import Decimal

import factory
from django.contrib.auth.models import User
from django.utils import timezone
from factory.django import DjangoModelFactory

from employees.models import Employee
from restaurants.models import Menu, MenuItem, Restaurant
from voting.models import Vote


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.django.Password('test1234')


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Employee {n}')


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.Sequence(lambda n: f'Restaurant {n}')
    opening_time = time(10, 0)
    closing_time = time(18, 0)


class MenuFactory(DjangoModelFactory):
    class Meta:
        model = Menu

    restaurant = factory.SubFactory(RestaurantFactory)
    date = factory.LazyFunction(timezone.localdate)
    title = factory.Sequence(lambda n: f'Menu {n}')


class MenuItemFactory(DjangoModelFactory):
    class Meta:
        model = MenuItem

    menu = factory.SubFactory(MenuFactory)
    name = factory.Sequence(lambda n: f'Dish {n}')
    price = Decimal('9.99')


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    employee = factory.SubFactory(EmployeeFactory)
    menu = factory.SubFactory(MenuFactory)
    date = factory.LazyAttribute(lambda vote: vote.menu.date)
