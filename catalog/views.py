from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from catalog.forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/login/'
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверяем, что пользователь - владелец или модератор
    if request.user == product.owner or request.user.has_perm('products.delete_product'):
        product.delete()
        messages.success(request, 'Продукт удален!')
    else:
        messages.error(request, 'У вас нет прав на удаление этого продукта!')

    return redirect('product_list')


@login_required
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверяем, что пользователь - модератор
    if request.user.has_perm('products.can_unpublish_product'):
        product.is_published = False
        product.save()
        messages.success(request, 'Публикация отменена!')
    else:
        messages.error(request, 'У вас нет прав на отмену публикации!')

    return redirect('product_list')