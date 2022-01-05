from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, CreateAPIView, \
    RetrieveAPIView


from news.api.serializers import PostSerializer, RubricSerializer, RubricPostSerializer
from news.models import Post, Rubric


class PostsListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'text']
    filter_fields = ['rubric', ]
    ordering_fields = ['user', 'rubric']


class PostCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDeleteApiView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class RubricListApiView(ListAPIView):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()


class RubricPostApiView(RetrieveAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricPostSerializer


class RubricCreateApiView(CreateAPIView):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()


class RubricDeleteApiView(RetrieveDestroyAPIView):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer