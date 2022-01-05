from django.urls import path


from shop.views import Home, Item, CreateItem

app_name = 'shop'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('item/<int:pk>',Item.as_view(),name='item_detail'),
    path('crate_item',CreateItem.as_view(),name='create_item'),
]
