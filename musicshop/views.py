from django.contrib import messages
from django.contrib.auth.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
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
        self.load_cart()
        if self.request.GET:
            print(f"GET: {request.GET}")
            if self.request.GET['sort']:
                self.sort_order = self.request.GET['sort']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.load_cart()
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

    def get(self, request, *args, **kwargs):
        self.load_cart()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.load_cart()
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

class CartPage(LoginRequiredMixin, CartManagerMixin, TemplateView):
    template_name = "musicshop/cart.html"
    login_url = reverse_lazy('login')
    sort_order = ""
    search_query = ""
    order_form = OrderForm()
    user_form = CreateUserForm()

    def get(self, request, *args, **kwargs):
        self.load_cart()
        print(request.session['cart_dict'])
        print('session')
        if self.request.GET:
            print(f"GET: {request.GET}")
            if self.request.GET['sort']:
                self.sort_order = self.request.GET['sort']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.load_cart()
        print(f"POST: {request.POST}")
        if (request.POST.get('search')):
            self.search_query = request.POST.get('search_field', "")

        if (request.POST.get('create_order')):
            self.order_form = OrderForm(request.POST)
            if self.order_form.is_valid():
                print("VALID ORDER_FORM")

                if not self.getIds():
                    messages.info(request, "Заказ не может быть составлен, если нет товаров в корзине")
                else:
                    try:
                        answer = self.order_form.save(self.cart_dict)
                        if answer:
                            print("HIIIIIIIIIIIII")
                            self.cart_dict = {}
                            request.session['cart_dict'] = {}
                            request.session.modified = True
                            self.order_form = OrderForm()
                            return redirect('index')
                    except Exception as e:
                        messages.info(request, "Системная ошибка. Заказ не был добавлен. Свяжитесь с администратором")
                        print(e)

            else:
                print("INVALID ORDER_FORM")
                print(self.order_form.cleaned_data)
                messages.info(request, "Отмена добавления заказа. Проверьте корректность заполнения полей")
                print(self.order_form.errors)



        if (request.POST.get('create_user')):
            self.user_form = CreateUserForm(request.POST)
            if self.user_form.is_valid():
                print("VALID USER_FORM")
                self.user_form.save()
            else:
                print("INVALID USER_FORM")
                print(self.user_form.errors)
                messages.error(request, "Отмена создания пользователя. Проверьте корректность заполнения полей")

        super().post(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)


    def get_queryset(self):
        objects = Catalog.objects.filter(pk__in = self.getIds())
        if(self.search_query):
            objects = objects.annotate(
                search=SearchVector('name', 'vendor', 'vendor_code')).filter(search=self.search_query)
        return objects


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        objects = Catalog.objects.filter(pk__in = self.getIds())
        if(self.search_query):
            objects = objects.annotate(
                search=SearchVector('name', 'vendor', 'vendor_code')).filter(search=self.search_query)

        context['title'] = 'index'
        context['show_cart'] = False
        context['sort_order'] = self.sort_order
        context['cart'] = self.cart_dict
        context['cart_items'] = objects
        context['num_items'] = self.calc_items_in_cart()
        context['cost'] = self.calc_total_cost()
        context['orderForm'] = self.order_form
        context['createUserForm'] = self.user_form
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