from rest_framework import generics, permissions
from .serializers import EmployeeSerializer


class CreateEmployeeView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.AllowAny]
