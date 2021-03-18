
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Post
from .serializers import PostSerializer, CreatePostSerializer,UpdatePostSerializer


class ListPostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)


class CreatePostView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UpdatePostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (JSONWebTokenAuthentication,)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, liked=self.request.data['liked'])


class RetrievePostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
