from django.urls import path
from .views import VoteView, TodayResultsView

urlpatterns = [
    path('vote/', VoteView.as_view(), name='vote'),
    path('results/today/', TodayResultsView.as_view(), name='results-today'),
]
