from rest_framework import serializers
from .models import Vote
from django.db import IntegrityError


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'menu']

    def create(self, validated_data):
        employee = self.context['request'].user.employee
        try:
            vote = Vote.objects.create(employee=employee, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError("You have already voted for this menu.")
        return vote


class VoteResultSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    menu_title = serializers.CharField()
    restaurant = serializers.CharField()
    votes = serializers.IntegerField()
