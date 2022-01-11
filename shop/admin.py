from django.contrib import admin

from shop.models import *


class ItemAdmin(admin.ModelAdmin):
    fields = ('slug','title', 'content', 'sale', 'price', 'category', 'image')

    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Item,ItemAdmin)
admin.site.register(Category)
