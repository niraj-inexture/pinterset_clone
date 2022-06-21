from django.shortcuts import render, redirect
from django.views import View
from image_post.models import ImageStore
from topic.models import Topic


# This class view is used to get trending topics
class TrendingTopicClassView(View):
    def get(self, request):
        if request.user.is_authenticated:
            trending_topic_data = Topic.objects.all().order_by('-total_likes')[:3]
            return render(request, 'topic/trending_topics.html', {'trending_topic_data': trending_topic_data})
        else:
            return redirect('index')


# This class view is used to get particular trending topic all images
class TrendingTopicImageClassView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            trending_topic_image_data = ImageStore.objects.filter(topic=id)
            return render(request, 'user/home.html', {'images': trending_topic_image_data})
        else:
            return redirect('index')
