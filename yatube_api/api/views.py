from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Comment, Follow
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    PostSerializer, CommentSerializer,
    GroupSerializer, FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(
            Post,
            pk=post_id
        )

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )
        serializer.save(
            post_id=post.id,
            author=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            post_id=self.kwargs.get('post_id'),
            author=self.request.user
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def create(self, request, *args, **kwargs):
        if request.data.get('following') == request.user.username:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
