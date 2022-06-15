from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.RegisterClassView.as_view(),name='register'),
    path('login/',views.LoginClassView.as_view(),name='login'),
    path('logout/',views.LogoutClassView.as_view(),name='logout'),
    path('home/',views.HomeClassView.as_view(),name='home'),
    path('user-profile/', views.ProfileClassView.as_view(), name='profile'),
    path('change-password/',views.ChangePasswordView.as_view(),name='change-password'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),name='password_reset'),
    path('forget-password/done/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
]