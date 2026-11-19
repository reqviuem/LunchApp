from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import generics, permissions

from .models import Menu, Restaurant
from .permissions import IsAdminOrReadOnly
from .serializers import MenuSerializer, RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]


class MenuCreateView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAdminUser]


class TodayMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Menu]:
        return (
            Menu.objects
            .filter(date=timezone.localdate())
            .select_related('restaurant')
            .prefetch_related('items')
        )
