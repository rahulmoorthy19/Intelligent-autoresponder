from django.urls import path
from . import views

urlpatterns = [
    path('', views.complain_page, name='complain_page'),
]
