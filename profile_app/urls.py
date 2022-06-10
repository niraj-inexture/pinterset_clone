from django.urls import path, include
from . import views

urlpatterns = [
    path('user-profile/<int:id>/', views.ProfileClassView.as_view(), name='profile'),
]