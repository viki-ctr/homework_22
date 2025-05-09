from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from catalog.forms import ProductForm

from .models import Product
from .services import get_all_products, get_products_by_category


class HomeView(ListView):
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return get_all_products()


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductListView(ListView):
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return get_all_products()


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = "/login/"
    success_url = reverse_lazy("catalog:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user == product.owner or request.user.has_perm("products.delete_product"):
        cache.delete("all_products_list")
        cache.delete(f"products_category_{product.category.slug}")
        product.delete()
        messages.success(request, "Продукт удален!")
    else:
        messages.error(request, "У вас нет прав на удаление этого продукта!")

    return redirect("catalog:product_list")


@login_required
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.has_perm("products.can_unpublish_product"):
        cache.delete("all_products_list")
        cache.delete(f"products_category_{product.category.slug}")
        product.is_published = False
        product.save()
        messages.success(request, "Публикация отменена!")
    else:
        messages.error(request, "У вас нет прав на отмену публикации!")

    return redirect("catalog:product_list")


@cache_page(60 * 10)
def category_products(request, category_slug):
    products = get_products_by_category(category_slug)
    return render(request, "catalog/category.html", {"products": products, "category_slug": category_slug})
