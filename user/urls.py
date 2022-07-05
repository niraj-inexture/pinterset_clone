from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.RegisterClassView.as_view(),name='register'),
    path('login/',views.LoginClassView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='user/index.html'),name='logout'),
    path('home/',views.HomeClassView.as_view(),name='home'),
    path('user-profile/', views.ProfileClassView.as_view(), name='profile'),
    path('change-password/',views.ChangePasswordView.as_view(),name='change-password'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),name='password_reset'),
    path('forget-password/done/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
    path('delete-account/<int:id>',views.DeleteAccountClassView.as_view(),name='delete-account'),
    path('search/',views.SearchClassView.as_view(),name='search-topic'),
    path('topic-list/',views.TopicListClassView.as_view(),name='topic-list'),
    path('deactivate-accunt/<int:id>',views.DeactivateUserAccountClassView.as_view(),name='deactivate-account'),
    path('activate-account/',views.ActivateUserAccountClassView.as_view(),name='activate-account'),
    path('activate/<uidb64>/<token>/',views.ActivateAccountClassView.as_view(), name='activate'),
    path('show-board/', views.CreateBoardClassView.as_view(), name='show-board'),
    path('create-board/',views.CreateBoardClassView.as_view(),name='create-board'),
    path('boards-image/<int:pk>',views.ShowImagesInBoardClassView.as_view(),name='boards-image'),
    path('delete-board-post/',views.DeleteBoardImageClassView.as_view(),name='delete-board-post'),
    path('delete-board/',views.DeleteBoardClassView.as_view(),name='delete-board')
]