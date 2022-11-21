from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment
from .permisssion import IsObjectOwner
from .serializer import User, UserSerializer, PostSerializer, PostLikeSerializer, CommentSerializer, AllPostSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from base import response
from base.services import create_update_record


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        return queryset

    @action(methods=['POST'], detail=False)
    def follow(self, request):
        data = request.data.copy()
        follow_user_id = data.get('user_id', )
        user_list = []
        if not follow_user_id:
            return response.BadRequest({'detail': 'User_id of follower is required'})
        follow_data = User.objects.get(id=self.request.user.id)
        for user in follow_data.following.all():
            user_list.append(user.id)
        user_list.append(follow_user_id) if follow_user_id not in user_list else None
        following_data = {
            'id': self.request.user.id,
            'following': user_list
        }
        create_update_record(following_data, UserSerializer, User)
        user_list.clear()
        follower_data = User.objects.get(id=follow_user_id)
        for user in follower_data.follower.all():
            user_list.append(user.id)
        user_list.append(self.request.user.id)
        follower_data = {
            'id': follow_user_id,
            'follower': user_list
        }
        create_update_record(follower_data, UserSerializer, User)
        return response.Ok({'detail': "You followed " + follow_data.username})

    @action(methods=['POST'], detail=False)
    def unfollow(self, request):
        data = request.data.copy()
        unfollow_user_id = data.get('user_id', )
        user_list = []
        if not unfollow_user_id:
            return response.BadRequest({'detail': 'User_id to unfollow user is required'})

        logged_in_data = User.objects.get(id=self.request.user.id)
        for user in logged_in_data.following.all():
            user_list.append(user.id)
        user_list.remove(unfollow_user_id) if unfollow_user_id in user_list else None

        logged_in_set = {
            'id': self.request.user.id,
            'following': user_list
        }
        create_update_record(logged_in_set, UserSerializer, User)

        user_list.clear()

        unfollow_user_data = User.objects.get(id=unfollow_user_id)
        for user in unfollow_user_data.follower.all():
            user_list.append(user.id)
        user_list.remove(self.request.user.id) if self.request.user.id in user_list else None
        following_set = {
            'id': unfollow_user_id,
            'follower': user_list
        }
        create_update_record(following_set, UserSerializer, User)
        return response.Ok({'detail': "You unfollowed " + unfollow_user_data.username})


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsObjectOwner]

    @action(methods=['GET'], detail=False)
    def all(self, request):
        queryset = self.queryset
        queryset = queryset.order_by('-created_at')
        return response.Ok(AllPostSerializer(queryset, many=True).data)

    @action(methods=['POST'], detail=False)
    def like(self, request):
        data = request.data.copy()
        post_id = data.get('post_id', )
        post = Post.objects.filter(id=post_id).first()
        print(post)
        if not post:
            return response.BadRequest({'Error Detail': 'Valid Post Id is required'})
        post_like = []
        for like in post.likes.all():
            post_like.append(like.id)
        post_like.append(self.request.user.pk) if self.request.user.id not in post_like else None
        print(post_like)
        post_data = {
            'id': post_id,
            'no_of_likes': len(post_like),
            'likes': post_like
        }
        return response.Ok(create_update_record(post_data, PostLikeSerializer, Post))

    @action(methods=['POST'], detail=False)
    def unlike(self, request):
        data = request.data.copy()
        post_id = data.get('post_id', )
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return response.BadRequest({'Error Detail': 'Valid Post Id is required'})
        post_like = []
        for like in post.likes.all():
            post_like.append(like.id)
        post_like.remove(self.request.user.id) if self.request.user.id in post_like else None
        post_data = {
            'id': post_id,
            'no_of_likes': len(post_like),
            'likes': post_like
        }
        print(post_data)
        return response.Ok(create_update_record(post_data, PostLikeSerializer, Post))


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
