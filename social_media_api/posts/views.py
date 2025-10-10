from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment, Like  # Added Like model import
from .serializers import PostSerializer, CommentSerializer
from notifications.utils import create_notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    user = request.user
    followed_users = user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        if post.author != user:
            create_notification(recipient=post.author, actor=user, verb="liked your post", target=post)

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        deleted, _ = Like.objects.filter(user=user, post=post).delete()
        if not deleted:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
