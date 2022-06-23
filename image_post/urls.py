from django.urls import path
from . import views

urlpatterns = [
    path('upload-image/', views.UploadImageClassView.as_view(), name='upload-image'),
    path('image-detail/<int:pk>', views.ImageDetailView.as_view(), name='image-detail'),
    path('save-image-detail/', views.SaveImageDetailView.as_view(), name='save-image'),
    path('delete-save-post/',views.DeleteSaveImageView.as_view(),name='delete-save-post'),
    path('delete-all-save-post/',views.DeleteAllSaveImageView.as_view(),name='delete-all-save-post'),
    path('update-save-post/<int:id>',views.UpdateImageDescriptionView.as_view(),name='update-save-post'),
    path('follow/', views.FollowClassView.as_view(),name='follow'),
    path('unfollow/', views.UnfollowClassView.as_view(),name='unfollow')
]