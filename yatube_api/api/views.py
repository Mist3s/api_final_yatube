from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Comment, Follow
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
        serializer.save(
            author=self.request.user
        )


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
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )
        serializer.save(
            post=post,
            author=self.request.user
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def get_queryset(self):
        return self.request.user.follower.all()
