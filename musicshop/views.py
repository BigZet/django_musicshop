from django.contrib.auth.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.detail import SingleObjectMixin

from musicshop.forms import *
from musicshop.models import *

# Create your views here.
from musicshop.utils import CartMixin, CartManagerMixin


def test_base(request):
    return render(request, 'musicshop/base.html',
                  {
                      'title': 'test_base',
                      'show_cart':True,
                      'selected_category':100
                  })


class CatalogPage(LoginRequiredMixin, CartManagerMixin, ListView):
    model = Catalog
    template_name = "musicshop/catalog.html"
    context_object_name = 'catalog_items'
    login_url = reverse_lazy('login')
    sort_order = ""
    category_slug = ""
    search_query = ""

    def get(self, request, *args, **kwargs):
        if self.request.GET:
            print(f"GET: {request.GET}")
            if self.request.GET['sort']:
                self.sort_order = self.request.GET['sort']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST:
            print(f"POST: {request.POST}")
            if (request.POST.get('search')):
                self.search_query = request.POST.get('search_field', "")

        super().post(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'index'
        context['show_cart'] = True
        context['sort_order'] = self.sort_order
        context['category_slug'] = self.category_slug
        context['cart'] = self.cart_dict
        context['num_items'] = self.calc_items_in_cart()
        context['cost'] = self.calc_total_cost()
        return context

    def get_queryset(self):
        self.category_slug = self.kwargs.get('category_slug')
        objects = self.model.objects.all()
        if(self.category_slug):
            objects = objects.filter(category__slug=self.kwargs.get('category_slug'))
        if(self.search_query):
            objects = objects.annotate(
                search=SearchVector('name', 'vendor', 'vendor_code')).filter(search=self.search_query)
        return objects

class ItemPage(LoginRequiredMixin, CartManagerMixin, DetailView):
    model = Catalog
    slug_url_kwarg = "item_slug"
    context_object_name = 'item'
    template_name = "musicshop/item_about.html"
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        if request.POST:
            print(f"POST: {request.POST}")

        super().post(request, *args, **kwargs)

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ItemPage, self).get_context_data(**kwargs)
        self.category_slug = self.kwargs.get('category_slug')
        context['title'] = 'О товаре'
        context['show_cart'] = True
        context['category_slug'] = self.category_slug
        context['num_items'] = self.calc_items_in_cart()
        context['cost'] = self.calc_total_cost()
        return context

class CartPage(LoginRequiredMixin, CartManagerMixin, ListView):
    model = Catalog
    template_name = "musicshop/cart.html"
    context_object_name = 'cart_items'
    login_url = reverse_lazy('login')
    sort_order = ""
    search_query = ""

    def get(self, request, *args, **kwargs):
        if self.request.GET:
            print(f"GET: {request.GET}")
            if self.request.GET['sort']:
                self.sort_order = self.request.GET['sort']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(f"POST: {request.POST}")
        if (request.POST.get('search')):
            self.search_query = request.POST.get('search_field', "")

        super().post(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)


    def get_queryset(self):
        objects = self.model.objects.filter(pk__in = self.getIds())
        if(self.search_query):
            objects = objects.annotate(
                search=SearchVector('name', 'vendor', 'vendor_code')).filter(search=self.search_query)
        return objects


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'index'
        context['show_cart'] = False
        context['sort_order'] = self.sort_order
        context['cart'] = self.cart_dict
        context['num_items'] = self.calc_items_in_cart()
        context['cost'] = self.calc_total_cost()
        return context


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "musicshop/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['show_cart'] = False
        context['authorized'] = False
        return context

    def get_success_url(self):
        return reverse_lazy('index')





def cart_test(request):
    sort_order = ''
    if request.GET:
        if request.GET['sort']:
            sort_order = request.GET['sort']
    return render(request, 'musicshop/cart.html',
                  {
                      'title': 'catalog_without',
                      'show_cart': False,
                      'selected_category':2,
                      'sort_order': sort_order
                  })