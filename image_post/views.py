from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from chat.models import Thread
from image_post.forms import UploadImageForm, ImageSaveForm, UpdateImageDescriptionForm
from image_post.models import ImageStore, ImageSave, ImageLike, Comment, BoardImages
from topic.models import Topic
from user.models import FollowPeople, RegisterUser, Boards


# Create your views here.

class SaveImageDetailView(View):
    """This class view is used to show saved images"""
    def get(self, request):
        if request.user.is_authenticated:
            save_img_data = ImageSave.objects.filter(user=request.user.id)
            return render(request, 'image_post/save_image.html',
                          {"save_img_data": save_img_data})
        else:
            return redirect('index')


class ImageDetailView(View):
    """This class view is used show detail of particular image and save this particular image"""
    def get(self, request, pk):
        if request.user.is_authenticated:
            image_store_obj = ImageStore.objects.get(pk=pk)
            union_obj = ImageStore.objects.none()
            for i in image_store_obj.topic.all():
                filtered_image_store_obj = ImageStore.objects.filter(approve_status=True,
                                                             image_type='Public').exclude(topic=i.id)
                union_obj = union_obj | filtered_image_store_obj
            save_data = ImageSaveForm(initial={'user': request.user.id, 'image_path': pk, 'is_save': True})
            save_user_data = ImageSave.objects.filter(user=request.user.id, image_path=pk).first()
            follower_data = FollowPeople.objects.filter(follow_user=image_store_obj.user.id).count()
            validate_follow_btn = FollowPeople.objects.filter(user=request.user.id, follow_user=image_store_obj.user.id)
            validate_like_btn = ImageLike.objects.filter(user=image_store_obj.user.id, like_user=request.user.id,
                                                         image_path=image_store_obj.id)
            total_likes = ImageLike.objects.filter(image_path=pk).count()
            comment_data = Comment.objects.filter(image_path=pk)
            boards_obj = Boards.objects.filter(user=request.user.id)

            return render(request, 'image_post/imagestore_detail.html',
                          {"one_data": image_store_obj,'all_data': union_obj, 'forms': save_data,
                           'save_user_data': save_user_data, 'follower_data': follower_data,
                           'validate_follow_btn': validate_follow_btn, 'validate_like_btn': validate_like_btn,
                           'comment_data':comment_data,'total_likes':total_likes,
                           'boards_name':boards_obj})
        else:
            return redirect('index')

    def post(self, request, pk):
        save_data = ImageSaveForm(request.POST)
        if save_data.is_valid():
            save_data.save()
            return redirect('image-detail', pk=pk)


class UploadImageClassView(View):
    """This class view is used to upload image"""
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


class DeleteSaveImageView(View):
    """This class view is used to delete particular image"""
    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('sid')
            save_image = ImageSave.objects.get(user=request.user.id, image_path=id)
            save_image.delete()
            return JsonResponse({'status': 1})
        else:
            return redirect('index')


class DeleteAllSaveImageView(View):
    """This class view is used to delete all image"""
    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('uid')
            save_image = ImageSave.objects.filter(user=id)
            save_image.delete()
            return JsonResponse({'status': 1})
        else:
            return redirect('index')


class UpdateImageDescriptionView(View):
    """This class view is used to update image description"""
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


class FollowClassView(View):
    """This class view is used to follow user"""
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.POST['uid']
            follow_user_id = request.POST['fid']
            user = RegisterUser.objects.get(id=user_id)
            follow_user = RegisterUser.objects.get(id=follow_user_id)
            follow = FollowPeople(user=user, follow_user=follow_user)
            follow.save()
            lookup1 = Q(first_person=request.user.id) & Q(second_person=request.user.id)
            lookup2 = Q(first_person=follow_user_id) & Q(second_person=follow_user_id)
            lookup = Q(lookup1 | lookup2)
            qs = Thread.objects.filter(lookup)
            if not qs.exists():
                second_person_obj = RegisterUser.objects.get(id=follow_user_id)
                Thread(first_person=request.user,second_person=second_person_obj).save()
            total_followers = FollowPeople.objects.filter(follow_user=follow_user_id).count()
            return JsonResponse({'status': 1, 'data': total_followers})
        else:
            return redirect('index')


class UnfollowClassView(View):
    """This class view is used to unfollow user"""
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.POST['uid']
            follow_user_id = request.POST['fid']
            follow = FollowPeople.objects.get(user=user_id, follow_user=follow_user_id)
            follow.delete()
            lookup1 = Q(first_person=request.user.id) & Q(second_person=request.user.id)
            lookup2 = Q(first_person=follow_user_id) & Q(second_person=follow_user_id)
            lookup = Q(lookup1 | lookup2)
            qs = Thread.objects.filter(lookup)
            if not qs.exists():
                second_person_obj = RegisterUser.objects.get(id=follow_user_id)
                Thread.objects.get(first_person=request.user, second_person=second_person_obj).delete()
            total_followers = FollowPeople.objects.filter(follow_user=follow_user_id).count()
            return JsonResponse({'status': 1, 'data': total_followers})
        else:
            return redirect('index')


class ImageHistoryClassView(View):
    """This class view is used to show image history and delete uploaded image"""
    def get(self, request):
        upload_image_data = ImageStore.objects.filter(user=request.user.id)
        return render(request, 'image_post/upload_image_history.html', {'upload_image_data': upload_image_data})

    def post(self, request):
        id = request.POST.get('imgid')
        delete_image = ImageStore.objects.get(id=id)
        delete_image.delete()
        return JsonResponse({'status': 1})


class LikeClassView(View):
    """ This class view is used to like post"""
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
            for topic in like_img.topic.all():
                like = topic.total_likes
                like += 1
                topic.total_likes = like
                topic.save()
            return JsonResponse({'status': 1, 'data': total_likes})
        else:
            return redirect('index')


class UnlikeClassView(View):
    """This class view is used to unlike post"""
    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.POST['uid']
            like_user_id = request.POST['fid']
            img_id = request.POST['imgid']
            like_img = ImageStore.objects.get(id=img_id)
            follow = ImageLike.objects.get(user=user_id, like_user=like_user_id, image_path=img_id)
            follow.delete()
            total_likes = ImageLike.objects.filter(image_path=img_id).count()
            for topic in like_img.topic.all():
                like = topic.total_likes
                like -= 1
                topic.total_likes = like
                topic.save()
            return JsonResponse({'status': 1, 'data': total_likes})
        else:
            return redirect('index')


class CommentClassView(View):
    """This view class is used to add comment"""
    def post(self, request):
        user_id = request.POST['uid']
        img_id = request.POST['imgid']
        comment = request.POST['comment']
        img_obj = ImageStore.objects.get(id=img_id)
        Comment(user=request.user, image_path=img_obj, comment=comment).save()
        return JsonResponse({'status': 1})


class DeleteCommentClassView(View):
    """This class view is used to delete comment"""
    def post(self, request):
        comment = request.POST['cid']
        cmt = Comment.objects.get(id=comment)
        cmt.delete()
        return JsonResponse({'status': 1})


class ImageSaveToBoardClassView(View):
    """This view class is used to save images in particular one board"""

    def post(self, request):
        if request.user.is_authenticated:
            board_id = request.POST['board_id']
            board_image_id = request.POST['board_image_id']
            board_image_filter = BoardImages.objects.filter(user=request.user.id, image_post=board_image_id, topic=board_id).first()
            if board_image_filter:
                messages.error(request,'You already enter this image in this topic')
                return JsonResponse({'status': 0})
            else:
                topic_obj = Topic.objects.get(id=board_id)
                image_obj = ImageStore.objects.get(id=board_image_id)
                board_images_obj = BoardImages(user=request.user, image_post=image_obj, topic=topic_obj)
                board_images_obj.save()
                return JsonResponse({'status': 1})
        else:
            return redirect('index')





