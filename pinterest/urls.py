from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from registration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexClassView.as_view()),
    path('registration/',include('registration.urls')),
    path('web-home/',include('home.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
