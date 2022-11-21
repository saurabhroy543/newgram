from accounts.viewsets import UserViewSet, PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


# creating Router object
router = DefaultRouter()


# Register view set with router
router.register('user', UserViewSet, basename='User_API_v1')
router.register('post', PostViewSet, basename='Post_API_v1')
router.register('comment', CommentViewSet, basename='Comment_API_v1')

