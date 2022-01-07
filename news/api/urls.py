from django.urls import path

from news.api.views import PostsListApiView, PostDeleteApiView, PostUpdateApiView, PostCreateApiView, RubricListApiView, \
    RubricPostApiView, RubricCreateApiView, RubricDeleteApiView, CommentApiView, PostDetailView, AddCommentApiView, \
    RatingApiView

urlpatterns = [
    path('posts/', PostsListApiView.as_view(), name='posts'),
    path('post/<int:pk>',PostDetailView.as_view()),
    path('post_create', PostCreateApiView.as_view(), name='create'),
    path('post_update/<int:pk>', PostUpdateApiView.as_view(), name='update'),
    path('post_delete/<int:pk>', PostDeleteApiView.as_view(), name='delete'),
    path('rubrics',RubricListApiView.as_view(),name='rubrics'),
    path('rubric/<int:pk>',RubricPostApiView.as_view(),name='rubric'),
    path('rubric_create',RubricCreateApiView.as_view()),
    path('rubric_delete/<int:pk>',RubricDeleteApiView.as_view()),
    path('comment/',CommentApiView.as_view()),
    path('add_comment/',AddCommentApiView.as_view()),
    path('do_rating/<int:post_pk>',RatingApiView.as_view()),
]
