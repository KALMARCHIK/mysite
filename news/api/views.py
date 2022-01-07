from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, CreateAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from news.api.serializers import PostSerializer, RubricSerializer, RubricPostSerializer, CommentSerializer, \
    PostRelationsSerializer, RatingSerializer, LikeSerializer
from news.models import Post, Rubric, Comment, Rating, Like


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


class PostDetailView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = PostRelationsSerializer(Post.objects.get(pk=kwargs.get('pk')))
        return Response(serializer.data, status=HTTP_200_OK)


class AddCommentApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        print(kwargs.get('post_pk'))
        data = {
            'rating': request.data['rating'],
            'post': int(kwargs.get('post_pk')),
            'user': request.user.id
        }
        serializer = RatingSerializer(data=data)

        if not Rating.objects.filter(post=data['post'], user=data['user']):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.is_valid():
                rating = Rating.objects.get(post=data['post'], user=data['user'])
                rating.rating = data['rating']
                rating.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class CommentApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikePostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        data = {
            'like': request.data['like'],
            'user': request.user.id,
            'post': kwargs.get('post_pk')
        }
        serializer = LikeSerializer(data=data)
        if not Like.objects.filter(post=data['post'], user=data['user']):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.is_valid():
                like = Like.objects.get(post=data['post'], user=data['user'])
                like.like = data['like']
                like.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
