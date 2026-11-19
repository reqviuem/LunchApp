from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import generics, permissions

from .models import Menu, Restaurant
from .serializers import MenuSerializer, RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self) -> list[permissions.BasePermission]:
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


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
