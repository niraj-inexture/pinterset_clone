from django.urls import path
from . import views

urlpatterns = [
    path('trending-topic/', views.TrendingTopicClassView.as_view(),name='trending-topic'),
    path('trending-topic-images/<int:id>',views.TrendingTopicImageClassView.as_view(),name='trending-topic-images')
]