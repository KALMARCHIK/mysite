from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Comment)
admin.site.register(AdvUser)
admin.site.register(Rubric)
admin.site.register(Post, PostAdmin)
admin.site.register(Rating)
admin.site.register(Like)
