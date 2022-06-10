from django.urls import path, include
from . import views

urlpatterns = [
    path('home-page/', views.HomeClassView.as_view(),name='home')
]