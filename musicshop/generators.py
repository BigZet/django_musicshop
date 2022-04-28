import random
from musicshop.models import *

def create_categories():
    names = [
        'Струнные',
        'Ударные',
        'Духовые',
        'Клавишные'
    ]
    c=1
    for i in names:
        Category.objects.create(name = i, cat_id = c)
        c+=1

def create_departments():
    names = [
        'Администрация',
        'Тех. поддержка',
        'Обслуживание клиента',
        'Бухгалтерия'
    ]

    for i in names:
        Department.objects.create(name = i)

def spawn_guitars(number):
    cat1 = Category.objects.get(cat_id=2)
    name = [
        "D-175 AC",
        "AD-555 NA SOUNDWAVE",
        "D-145 BK",
        "F-38 BK",
        "D-435 NA",
        "C-125",
        "Les Poul F-231",
        "Telecaster Cali - 02"
        ]
    vendors = [
        'Ibanez',
        'Flight',
        'Epiphone',
        'Gibson',
        'Fender',
        'Yamaha',
        'Vertisari'
    ]
    for i in range(number):
        Catalog.objects.create(name=random.choice(name), vendor=random.choice(vendors),
                               vendor_code=str(random.randint(10000, 99999)), price=random.randint(10000, 99999),
                               category_id=cat1)

