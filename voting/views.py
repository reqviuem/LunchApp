from django.db.models import Count, F
from django.utils import timezone
from rest_framework import generics, permissions, response, views
from employees.permissions import IsEmployee
from .models import Vote
from .serializers import VoteResultSerializer, VoteSerializer


class VoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsEmployee]


class TodayResultsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        results = (
            Vote.objects
            .filter(date=timezone.localdate())
            .annotate(menu_title=F('menu__title'), restaurant=F('menu__restaurant__name'))
            .values('menu_id', 'menu_title', 'restaurant')
            .annotate(votes=Count('id'))
            .order_by('-votes', 'menu_title')
        )
        return response.Response(VoteResultSerializer(results, many=True).data)
