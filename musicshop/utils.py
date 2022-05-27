import json

from django.contrib import messages

from .models import *
import warnings




class CartMixin:
    def add_to_cart(self, items):
        if not self.request.session.get('cart_ids', False):
            self.request.session['cart_ids'] = [i for i in items]
        else:
            self.request.session['cart_ids'].extend([i for i in items])
        self.request.session.modified = True

    def get_cart(self):
        if(self.request.session):
            return self.request.session.get('cart_ids', "None")
        return "None"



class CartManagerMixin:

    def __init__(self):
        self.cart_dict = {}


    def load_cart(self):
        self.cart_dict = self.request.session.get('cart_dict', {})


    def update_cart(self):
        for i in list(self.cart_dict.keys()):
            if self.cart_dict[i]<=0:
                self.cart_dict.pop(i)

        if not self.request.session.get('cart_dict', False):
            self.request.session['cart_dict'] = self.cart_dict
        else:
            self.request.session['cart_dict'].update(self.cart_dict)
        self.request.session.modified = True
        print(self.request.session['cart_dict'])
        print(self.cart_dict)

    def add_one(self, id, quantity):
        if not self.cart_dict.get(id):
            self.cart_dict[id] = 0
        if (self.cart_dict.get(id) + quantity > Catalog.objects.get(id=id).countAll()['all']):
            print(f"ПРЕВЫШЕНИЕ ЗАКАЗА (поймано в add) {id}")
            messages.info(self.request, f"Отмена добавления: в наличии всего {Catalog.objects.get(id=id).countAll()['all']} шт. товара {Catalog.objects.get(id=id).vendor.upper()} {Catalog.objects.get(id=id).name}")
            self.cart_dict[id] = Catalog.objects.get(id=id).countAll()['all']
        else:
            self.cart_dict[id] += quantity

        self.update_cart()


    def remove_one(self, id, quantity):
        if self.cart_dict.get(id):
            if self.cart_dict.get(id) - quantity < 0:
                self.cart_dict[id] = 0
            else:
                self.cart_dict[id] -= quantity
        self.update_cart()

    def add_dict(self, id_quantity:dict):
        for id in id_quantity.keys():
            self.add_one(id, id_quantity[id])

    def remove_dict(self, id_quantity:dict):
        for id in id_quantity.keys():
            self.remove_one(id, id_quantity[id])


    def add_list(self, ids):
        id_dict = {i:1 for i in ids}
        self.add_dict(id_dict)

    def remove_list(self, ids):
        id_dict = {i:1 for i in ids}
        self.remove_dict(id_dict)

    def remove_list_all(self, ids):
        id_dict = {i:self.cart_dict.get(i, 0) for i in ids}
        self.remove_dict(id_dict)


    def show_cart(self):
        print(self.cart_dict)

    def calc_items_in_cart(self):
        c = 0
        for i in self.cart_dict:
            c+=self.cart_dict[i]

        return c

    def calc_total_cost(self):
        c = 0
        for i in self.cart_dict:
            c+=Catalog.objects.get(id=i).price * self.cart_dict[i]

        return c

    def getIds(self):
        return self.cart_dict.keys()


    def post(self, request, *args, **kwargs):
        if request.POST.get('add_selected'):
            if request.POST.get('cbx_slave'):
                to_add_items = request.POST.getlist('cbx_slave')
                if to_add_items:
                    self.add_list(to_add_items)
        if request.POST.get('del_selected'):
            if request.POST.get('cbx_slave'):
                to_del_items = request.POST.getlist('cbx_slave')
                if to_del_items:
                    self.remove_list_all(to_del_items)

        to_add_item = request.POST.get("add_item")
        if to_add_item:
            self.add_list([to_add_item])

        to_del_item = request.POST.get("del_item")
        if to_del_item:
            self.remove_list([to_del_item])


