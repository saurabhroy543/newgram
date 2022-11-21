from rest_framework import serializers
from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username','following',
            'follower'
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_at')

    def validate(self, data):
        title = data.get('title')
        description = data.get('description')
        print(title, description)
        print(data)
        if not title or not description:
            raise serializers.ValidationError({'Error Detail': 'Title and description is required'})
        data['created_by'] = self.context['request'].user
        return data


class AllPostSerializer(serializers.ModelSerializer):
    comment_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_at', 'comment_data','no_of_likes')

    @staticmethod
    def get_comment_data(obj):
        queryset = Comment.objects.filter(post=obj.id)
        return CommentSerializer(queryset, many=True).data if obj.id else None

    def validate(self, data):
        title = data.get('title')
        description = data.get('description')
        print(title, description)
        print(data)
        if not title or not description:
            raise serializers.ValidationError({'Error Detail': 'Title and description is required'})
        data['created_by'] = self.context['request'].user
        return data


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'no_of_likes', 'likes')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        post = data.get('post')
        if not post:
            raise serializers.ValidationError({'Error detail': 'Post Id is required'})
        data['commented_by'] = self.context['request'].user
        return data
