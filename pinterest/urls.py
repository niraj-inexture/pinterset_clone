from django.contrib import admin
from django.urls import path,include
from registration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexClassView.as_view()),
    path('registration/',include('registration.urls')),
    path('web-home/',include('home.urls'))
]
