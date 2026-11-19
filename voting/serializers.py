from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'menu']

    def validate_menu(self, menu):
        if menu.date != timezone.localdate():
            raise serializers.ValidationError("You can only vote for today's menu.")
        return menu

    def validate(self, attrs):
        employee = self.context['request'].user.employee
        if Vote.objects.filter(employee=employee, date=timezone.localdate()).exists():
            raise serializers.ValidationError('You have already voted today.')
        return attrs

    def create(self, validated_data):
        employee = self.context['request'].user.employee
        try:
            with transaction.atomic():
                return Vote.objects.create(
                    employee=employee,
                    date=validated_data['menu'].date,
                    **validated_data,
                )
        except IntegrityError:
            raise serializers.ValidationError('You have already voted today.') from None


class VoteResultSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    menu_title = serializers.CharField()
    restaurant = serializers.CharField()
    votes = serializers.IntegerField()
