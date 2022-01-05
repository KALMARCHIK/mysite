from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from shop.forms import ItemForm
from shop.models import Item


class Home(ListView):
    template_name = 'shop/home.html'
    queryset = Item.objects.all()
    context_object_name = 'items'


class Item(DetailView):
    template_name = 'shop/item.html'
    queryset = Item.objects.all()
    context_object_name = 'item'


class CreateItem(CreateView):
    model = Item
    template_name = 'shop/create_item.html'
    form_class = ItemForm
    success_url = reverse_lazy('shop:home')
    def get_form(self):
        form = super().get_form()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
