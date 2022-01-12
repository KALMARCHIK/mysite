from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, TemplateView, ListView, CreateView, DetailView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Count
from django.views.generic.base import View
from .forms import *
from .mixins import PostChangeMixin

from .models import *
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'news/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'news/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("login")
    template_name = "news/register.html"

    def get_form(self):
        form = super().get_form()
        return form

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def formset_view(request):
    if request.method == 'POST':
        ProstoFormSet = formset_factory(ProstoForm, extra=2)
        formset = ProstoFormSet(request.POST)
        if formset.is_valid():
            a = 0

            while a < len(formset):
                title = formset[a].cleaned_data['title']
                text = formset[a].cleaned_data['text']
                print(title)
                print(text)
                Post.objects.create(title=title, text=text, rubric_id=7, user_id=12)
                a += 1
            return redirect('ass')
    else:
        ProstoFormSet = formset_factory(ProstoForm, extra=2)
        formset = ProstoFormSet
    context = {}
    context['formset'] = formset
    return render(request, "news/ass.html", context)


class RegisterDoneView(TemplateView):
    template_name = 'news/register_done.html'


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                             PasswordChangeView):
    template_name = 'news/change_password.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль пользователя изменен'


class LoginView(LoginView):
    template_name = 'news/login.html'


class PostView(ListView):
    model = Post
    queryset = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')
    template_name = 'news/home.html'
    context_object_name = 'posts'
    paginate_by = 4


class AboutView(TemplateView):
    template_name = 'news/about.html'


class ProstoView(View):
    template_name = 'news/ass1.html'
    formset = ProstoFormSet

    def get(self, request):

        return render(request, self.template_name, {'formset': self.formset})

    def post(self, request):
        form = self.formset(request.POST)
        if form.is_valid():
            a = 0

            while a < len(form):
                title = form[a].cleaned_data['title']
                text = form[a].cleaned_data['text']
                print(title)
                print(text)
                Post.objects.create(title=title, text=text, rubric_id=7, user_id=12)
                a += 1
            return redirect('ass1')


class PostCreateView(LoginRequiredMixin,CreateView):
    form_class = PostForm
    template_name = 'news/create.html'

    def get_form(self):
        form = super().get_form()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user_id=self.request.user)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'news/user_delete.html '
    success_url = reverse_lazy('home')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()

        return get_object_or_404(queryset, pk=self.user_id)


class AddRating(View):
    def post(self, request, pk):
        form = RatingForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            if not Rating.objects.filter(user=request.user, post=post):
                form.user = request.user
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Ваша оценка добавлена')
            else:
                rating = Rating.objects.get(user=request.user, post=post)
                rating.rating = request.POST.get('rating')
                rating.save()
                messages.add_message(request, messages.SUCCESS, 'Ваша оценка изменена')
        return redirect(post.get_absolute_url())


class AddLikeView(View):
    def post(self, request, pk):
        form = LikeForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            if not Like.objects.filter(post=post, user=request.user):
                form.user = request.user
                form.like = True
                form.save()
            else:
                like = Like.objects.get(post=post, user=request.user)
                if like.like == False:
                    like.like = True
                else:
                    like.like = False
                like.save()
        return redirect(post.get_absolute_url())


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):

        context = super().get_context_data()
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if Rating.objects.filter(post=post, user=self.request.user):
            user_rating = Rating.objects.get(post=post, user=self.request.user).rating
        else:
            user_rating = 'Вы не оставляли сво рейтинг'
        ratings = 0
        likes = 0
        if post.ratings.all():
            for rating in post.ratings.all():
                ratings += int(rating.rating)
            ratings = round(ratings / len(post.ratings.all()), 2)

        else:
            ratings = 'Никто не оставлял своей оценки.Будьте первыми'
        if post.likes.all():
            likes = len(post.likes.filter(like=True))
        if Like.objects.filter(post=post, user=self.request.user):
            user_like = Like.objects.get(post=post, user=self.request.user)

            context['user_like'] = user_like
        context['ratings'] = ratings
        context['likes'] = likes
        context['user_rating'] = user_rating
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.author = request.user.username
            form.save()
        return redirect(post.get_absolute_url())


class PostUpdateView(PostChangeMixin,UpdateView):
    model = Post
    template_name = 'news/post_change.html'
    fields = ['title', 'text', 'rubric']


class PostDeleteView(DeleteView):  # Создание нового класса
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('home')


class RubricView(ListView):
    model = Post
    template_name = 'news/rubric_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(rubric__id=self.kwargs['rubric_id'])


class SearchView(ListView):
    template_name = 'news/search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            Q(title__icontains=self.request.GET.get('q')) | Q(text__icontains=self.request.GET.get('q')))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class AddRubric(CreateView):
    model = Rubric
    template_name = 'news/add_rubric.html'
    form_class = RubricForm
    success_url = reverse_lazy('home')


class CommentDelete(View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        post = comment.post
        comment.delete()
        return redirect(post.get_absolute_url())


class UpdateComment(View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        post = comment.post
        comment.content = request.POST.get('content')
        comment.save()
        return redirect(post.get_absolute_url())