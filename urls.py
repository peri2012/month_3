from django.urls import path
from apps.users.views import index

urlpatterns = [
    path('', index, name='index_url')
]