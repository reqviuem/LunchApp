from django.urls import path
from .views import CreateEmployeeView

urlpatterns = [
    path('', CreateEmployeeView.as_view(), name='create-employee'),
]
