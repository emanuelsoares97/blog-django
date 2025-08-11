from django.urls import path
from .views import notifications_list

urlpatterns = [
    path('', notifications_list, name='notifications_list'),
]
