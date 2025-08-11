from django.urls import path
from . import views as user_views

urlpatterns = [
    path('inbox/', user_views.inbox, name='inbox'),
    path('<str:username>/', user_views.conversation, name='conversation'),
]
