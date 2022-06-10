from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterClassView.as_view(),name='register'),
    path('login/',views.LoginClassView.as_view(),name='login'),
    path('logout/',views.LogoutClassView.as_view(),name='logout')
]