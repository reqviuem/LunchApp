from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('employee', 'menu', 'date')
    list_filter = ('date',)
    search_fields = ('employee__name',)
