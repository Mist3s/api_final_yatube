from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import (
    Post, Group, Comment, Follow, User
)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=serializers.CurrentUserDefault(),
        required=False
    )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=serializers.CurrentUserDefault(),
        required=False
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'post',
            'text',
            'created'
        )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = (
            'user',
            'following',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]
