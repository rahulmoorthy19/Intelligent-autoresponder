from django.urls import path
from . import views

urlpatterns = [
    path('', views.complain_page, name='complain_page'),
    path('thankyou_page/', views.thankyou_page,name='thankyou_page')
]
