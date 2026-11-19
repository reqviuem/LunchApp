from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        write_only=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all(), message='A user with that username already exists.')],
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        validators=[validate_password],
    )

    class Meta:
        model = Employee
        fields = ['id', 'name', 'username', 'password']

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return Employee.objects.create(user=user, name=validated_data['name'])
