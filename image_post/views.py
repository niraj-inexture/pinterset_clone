from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from image_post.forms import UploadImageForm, ImageSaveForm, UpdateImageDescriptionForm
from image_post.models import ImageStore, ImageSave, ImageLike, Comment
from topic.models import Topic
from user.models import FollowPeople, RegisterUser


# Create your views here.

# This class view is used to show saved images
class SaveImageDetailView(View):
    def get(self, request):
        if request.user.is_authenticated:
            save_img_data = ImageSave.objects.filter(user=request.user.id)
            return render(request, 'image_post/save_image.html',
                          {"save_img_data": save_img_data})
        else:
            return redirect('index')


# This class view is used show detail of particular image and save this particular image
class ImageDetailView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            img_data = ImageStore.objects.get(pk=pk)
            all_related_img = ImageStore.objects.filter(topic_id=img_data.topic_id, approve_status=True,
                                                        image_type='Public')
            save_data = ImageSaveForm(initial={'user': request.user.id, 'image_path': pk, 'is_save': True})
            save_user_data = ImageSave.objects.filter(user=request.user.id, image_path=pk).first()
            follower_data = FollowPeople.objects.filter(follow_user=img_data.user.id).count()
            validate_follow_btn = FollowPeople.objects.filter(user=request.user.id, follow_user=img_data.user.id)
            validate_like_btn = ImageLike.objects.filter(user=img_data.user.id, like_user=request.user.id,
                                                         image_path=img_data.id)
            total_likes = ImageLike.objects.filter(image_path=pk).count()
            comment_data = Comment.objects.filter(image_path=pk)
            return render(request, 'image_post/imagestore_detail.html',
                          {"one_data": img_data, 'all_data': all_related_img, 'forms': save_data,
                           'save_user_data': save_user_data, 'follower_data': follower_data,
                           'validate_follow_btn': validate_follow_btn, 'validate_like_btn': validate_like_btn,
                           'comment_data':comment_data,'total_likes':total_likes})
        else:
            return redirect('index')

    def post(self, request, pk):
        save_data = ImageSaveForm(request.POST)
        if save_data.is_valid():
            save_data.save()
            return redirect('image-detail', pk=pk)


# This class view is used to upload image
class UploadImageClassView(View):
    def get(self, request):
        if request.user.is_authenticated:
            upload_image = UploadImageForm(initial={'user': request.user.id})
            return render(request, 'image_post/upload_image.html', {'forms': upload_image})
        else:
            return redirect('index')

    def post(self, request):
        upload_image = UploadImageForm(request.POST, request.FILES)
        if upload_image.is_valid():
            upload_image.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect('upload-image')
        else:
            return render(request, 'image_post/upload_image.html', {'forms': upload_image})


# This class view is used to delete particular image
class DeleteSaveImageView(View):
    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('sid')
            save_image = ImageSave.objects.get(user=request.user.id, image_path=id)
            save_image.delete()
            return JsonResponse({'status': 1})
        else:
            return redirect('index')


# This class view is used to delete all image
class DeleteAllSaveImageView(View):
    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('uid')
            save_image = ImageSave.objects.filter(user=id)
            save_image.delete()
            return JsonResponse({'status': 1})
        else:
            return redirect('index')


# This class view is used to update image description
class UpdateImageDescriptionView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            image_detail = ImageStore.objects.get(pk=id)
            upload_image = UpdateImageDescriptionForm(instance=image_detail)
            return render(request, 'image_post/update_image_detail.html', {'forms': upload_image})
        else:
            return redirect('index')

    def post(self, request, id):
        image_detail = ImageStore.objects.get(pk=id)
        upload_image = UpdateImageDescriptionForm(request.POST, instance=image_detail)
        if upload_image.is_valid():
            upload_image.save()
            messages.success(request, 'Image details updated successfully')
            return render(request, 'image_post/update_image_detail.html', {'forms': upload_image})
        else:
            return render(request, 'image_post/update_image_detail.html', {'forms': upload_image})


# This class view is used to follow user
class FollowClassView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.POST['uid']
            follow_user_id = request.POST['fid']
            user = RegisterUser.objects.get(id=user_id)
            follow_user = RegisterUser.objects.get(id=follow_user_id)
            follow = FollowPeople(user=user, follow_user=follow_user)
            follow.save()
            total_followers = FollowPeople.objects.filter(follow_user=follow_user_id).count()
            return JsonResponse({'status': 1, 'data': total_followers})
        else:
            return redirect('index')


# This class view is used to unfollow user
class UnfollowClassView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.POST['uid']
            follow_user_id = request.POST['fid']
            follow = FollowPeople.objects.get(user=user_id, follow_user=follow_user_id)
            follow.delete()
            total_followers = FollowPeople.objects.filter(follow_user=follow_user_id).count()
            return JsonResponse({'status': 1, 'data': total_followers})
        else:
            return redirect('index')


# This class view is used to show image history and delete uploaded image
class ImageHistoryClassView(View):
    def get(self, request):
        upload_image_data = ImageStore.objects.filter(user=request.user.id)
        return render(request, 'image_post/upload_image_history.html', {'upload_image_data': upload_image_data})

    def post(self, request):
        id = request.POST.get('imgid')
        delete_image = ImageStore.objects.get(id=id)
        delete_image.delete()
        return JsonResponse({'status': 1})


# This class view is used to like post
class LikeClassView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.POST['uid']
            like_user_id = request.POST['fid']
            img_id = request.POST['imgid']
            user = RegisterUser.objects.get(id=user_id)
            like_user = RegisterUser.objects.get(id=like_user_id)
            like_img = ImageStore.objects.get(id=img_id)
            follow = ImageLike(user=user, like_user=like_user, image_path=like_img)
            follow.save()
            total_likes = ImageLike.objects.filter(image_path=like_img).count()
            total_topic_like = Topic.objects.get(id=like_img.topic.id)
            like = total_topic_like.total_likes
            like += 1
            total_topic_like.total_likes = like
            total_topic_like.save()
            return JsonResponse({'status': 1, 'data': total_likes})
        else:
            return redirect('index')


# This class view is used to unlike post
class UnlikeClassView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.POST['uid']
            like_user_id = request.POST['fid']
            img_id = request.POST['imgid']
            like_img = ImageStore.objects.get(id=img_id)
            follow = ImageLike.objects.get(user=user_id, like_user=like_user_id, image_path=img_id)
            follow.delete()
            total_likes = ImageLike.objects.filter(image_path=img_id).count()
            total_topic_like = Topic.objects.get(id=like_img.topic.id)
            like = total_topic_like.total_likes
            like -= 1
            total_topic_like.total_likes = like
            total_topic_like.save()
            return JsonResponse({'status': 1, 'data': total_likes})
        else:
            return redirect('index')


# This view class is used to add comment
class CommentClassView(View):
    def post(self, request):
        user_id = request.POST['uid']
        img_id = request.POST['imgid']
        comment = request.POST['comment']
        img_obj = ImageStore.objects.get(id=img_id)
        Comment(user=request.user, image_path=img_obj, comment=comment).save()
        return JsonResponse({'status': 1})


# This class view is used to delete comment
class DeleteCommentClassView(View):
    def post(self, request):
        comment = request.POST['cid']
        cmt = Comment.objects.get(id=comment)
        cmt.delete()
        return JsonResponse({'status': 1})
