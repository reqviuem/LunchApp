from django.urls import path

from .views import MenuCreateView, RestaurantDetailView, RestaurantListCreateView, TodayMenuView

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurants'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('menus/', MenuCreateView.as_view(), name='menu-create'),
    path('menus/today/', TodayMenuView.as_view(), name='menu-today'),
]
