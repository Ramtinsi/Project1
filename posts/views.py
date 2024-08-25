

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Avg, Count
from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer

class PostListCreateView(APIView):
    def get(self, request):
        posts = Post.objects.annotate(
            average_rating=Avg('rating__score'),
            ratings_count=Count('rating')
        ).all()

        post_data = []
        for post in posts:
            user_rating = None
            if request.user.is_authenticated:
                try:
                    user_rating = Rating.objects.get(post=post, user=request.user).score
                except Rating.DoesNotExist:
                    user_rating = None

            post_data.append({
                "title": post.title,
                "content": post.content,
                "average_rating": post.average_rating,
                "ratings_count": post.ratings_count,
                "user_rating": user_rating
            })

        return Response(post_data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import HttpResponse
from posts.models import Post

def delete_all_posts(request):
    Post.objects.all().delete()
    return HttpResponse("All posts have been deleted.")

from rest_framework.permissions import AllowAny

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]






