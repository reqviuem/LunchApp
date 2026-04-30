from django.utils import timezone
from django.db.models import Count
from rest_framework import generics, views, permissions, response
from .models import Vote
from .serializers import VoteSerializer


class VoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class TodayResultsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self):
        today = timezone.now().date()
        results = (
            Vote.objects
            .filter(menu__date=today)
            .values('menu__id', 'menu__title', 'menu__restaurant__name')
            .annotate(votes=Count('id'))
            .order_by('-votes')
        )
        data = [
            {
                'menu_id': r['menu__id'],
                'menu_title': r['menu__title'],
                'restaurant': r['menu__restaurant__name'],
                'votes': r['votes'],
            }
            for r in results
        ]
        return response.Response(data)
