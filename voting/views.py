from django.utils import timezone
from django.db.models import Count
from rest_framework import generics, views, permissions, response, status
from .models import Vote
from .serializers import VoteSerializer



class VoteView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class TodayResultsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        results = (
            Vote.objects
            .filter(menu__date=today)
            .values('menu__id', 'menu__title', 'menu__restaurant__name')
            .annotate(votes=Count('id'))
            .order_by('-votes')
        )

        if not results.exists():
            return response.Response(
                {'detail': 'No votes have been cast today.'},
                status=status.HTTP_404_NOT_FOUND
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
        return response.Response(data, status=status.HTTP_200_OK)
