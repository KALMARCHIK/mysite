from django.urls import path

from .views import *
urlpatterns = [
    path('', PostView.as_view(), name='home'),  # получилось
    path('about/', AboutView.as_view(), name='about'),  # получилось
    path('accounts/login/', LoginView.as_view(), name='login'),  # получилось
    path('accounts/profile_change', ChangeUserInfoView.as_view(), name='profile_change'),  # получилось
    path('accounts/profile', ProfileView.as_view(), name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),  # получилось
    path('accounts/register', RegisterUser.as_view(), name='register'),
    path('accounts/register_dome',RegisterDoneView.as_view(),name='register_done'),
    path('accounts/change_password', UserPasswordChangeView.as_view(), name='change_password'),
    path('user_delete',DeleteUserView.as_view(),name='user_delete'),
    path('create_post', PostCreateView.as_view(), name='create_post'),  # получилось
    path('post_full/<int:pk>', PostDetailView.as_view(), name='post_full'),   # получилось
    path('post_change/<int:pk>', PostUpdateView.as_view(), name='post_change'),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path('rating/<int:pk>/',AddRating.as_view(),name="add_rating"),
    path('add_like/<int:pk>',AddLikeView.as_view(),name='add_like'),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('rubric_post/<int:rubric_id>', RubricView.as_view(), name='rubric_post'),  # получилось
    path('search',SearchView.as_view(),name='search'),
    path('add_rubric',AddRubric.as_view(),name='add_rubric'),
    path('ass',formset_view,name='ass'),
    path('ass1',ProstoView.as_view(),name='ass1'),
    path('delete_comment/<int:pk>',CommentDelete.as_view(),name='comment_delete'),
    path('update_comment/<int:pk>',UpdateComment.as_view(),name='update_comment'),
]
