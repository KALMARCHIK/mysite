from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AbstractUser


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, verbose_name='Рубрика', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey('AdvUser', on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_review(self):
        return Comment.objects.filter(post=self.id)

    def get_absolute_url(self):
        return reverse('post_full', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост',related_name='comments')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошёл активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения  о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass


class Rating(models.Model):
    rating = models.IntegerField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, blank=True, null=True, related_name='ratings')

    def __str__(self):
        return f'Рейтинг : {self.rating}, Пост : {self.post}, Пользователь : {self.user}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Like(models.Model):
    like = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'Рейтинг : {self.like}, Пост : {self.post}, Пользователь : {self.user}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
