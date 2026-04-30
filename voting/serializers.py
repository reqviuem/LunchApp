from rest_framework import serializers
from .models import Vote
from restaurants.serializers import MenuSerializer


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'menu']

    def create(self, validated_data):
        employee = self.context['request'].user.employee
        vote = Vote.objects.create(employee=employee, **validated_data)
        return vote


class VoteResultSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    menu_title = serializers.CharField()
    restaurant = serializers.CharField()
    votes = serializers.IntegerField()
