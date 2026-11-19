from rest_framework import generics, permissions

from myproject.throttles import RegistrationRateThrottle

from .serializers import EmployeeSerializer


class CreateEmployeeView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegistrationRateThrottle]
