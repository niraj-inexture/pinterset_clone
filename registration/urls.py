from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/', views.RegisterClassView.as_view(),name='register'),
    path('login/',views.LoginClassView.as_view(),name='login'),
    path('logout/',views.LogoutClassView.as_view(),name='logout')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)