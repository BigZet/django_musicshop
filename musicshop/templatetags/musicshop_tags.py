from django import template
from musicshop.models import *

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def getGoodQuantity(good, storage_type):
    if (not good):
        return 0
    else:
        return good.countAll()[storage_type]


@register.inclusion_tag('musicshop/list_categories.html')
def list_categories(category_slug = "strunnye"):
    categroies = Category.objects.all()
    return {
        'available_categories' : categroies,
        'category_slug': category_slug
    }

@register.inclusion_tag('musicshop/table_catalog.html')
def table_catalog(table_items, cart ="", sort_order='cost_up', table_type="catalog"):
    if sort_order == "cost_up":
        table_items = table_items.order_by('price')
    elif sort_order == "cost_down":
        table_items = table_items.order_by('-price')
    elif sort_order == "date_up":
        table_items = table_items.order_by('-add_time')
    elif sort_order == "date_down":
        table_items = table_items.order_by('add_time')
    elif sort_order == "name_down":
        table_items = table_items.order_by('-name')
    elif sort_order == "name_up":
        table_items = table_items.order_by('name')
    return {
        'table_items' : table_items,
        'table_type' : table_type,
        'cart':cart
    }

@register.inclusion_tag('musicshop/container_cart.html')
def container_cart(num_items, cost):
    # { % if num_items_mod10 == 1 %}
    # {{num_items}}
    # товар


# { % elif num_items_mod10 > 4 or num_items_mod10 == 0 %}
# {{num_items}}
# товаров
# { % else %}
# {{num_items}}
# товара
# { % endif %}
    return{
        'num_items':num_items,
        'cost':cost
    }

@register.filter(name = "get_correct_items_word")
def get_correct_items_word(num_items):
    word = "не указан"
    if num_items%100//10 == 1:
        word = "товаров"
    elif num_items%10 == 1:
        word="товар"
    elif num_items%10>4 or num_items%10 == 0:
        word = "товаров"
    else:
        word = "товара"
    return word

@register.filter(name='give_from_cart')
def give_from_cart(object, value):
    if object:
        return object.get(str(value), 0)
    else:
        return 0
