from django.urls import path
from .views import RestaurantListCreateView, MenuCreateView, TodayMenuView

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurants'),
    path('menus/', MenuCreateView.as_view(), name='menu-create'),
    path('menus/today/', TodayMenuView.as_view(), name='menu-today'),
]
