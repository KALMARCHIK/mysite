from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy

from news.models import Post


class PostChangeMixin(AccessMixin):
    login_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        post = Post.objects.get(pk=post_pk)
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif post.user is None:
            if not request.user.is_staff:
                return self.handle_no_permission()
        elif post.user != request.user:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
