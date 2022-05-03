from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from transliterate import slugify
# Create your models here.


class DISCOUNT (models.IntegerChoices):
    EMPTY = 0,  _('Отсутствует')
    STANDART = 1,  _('Стандартная')
    REGULAR_CUSTOMER = 2,  _('Постоянный покупатель')
    PROMO = 3,  _('Промо-акция')
    VIP = 4,  _('Особый клиент')

class GENDER (models.IntegerChoices):
    EMPTY = 0,  _('Не указано')
    FEMALE = 1,  _('Женщина')
    MALE = 2,  _('Мужчина')

class WARRANTY (models.IntegerChoices):
    EMPTY = 0,  _('Отсутсвует')
    STANDART = 1,  _('Стандартная')
    EXTRA = 2,  _('Особая')
    LONG = 3,  _('С возможностью продления')

class ORDER_STATUS (models.IntegerChoices):
    EMPTY = 0,  _('Не указан')
    INIT = 1,  _('Инициализация')
    OPENED = 2,  _('Открыт')
    CLOSED = 3,  _('Закрыт')
    ERRORHANDLED = 4,  _('Ошибка')
    DISCUSS = 5,  _('В стадии обсуждения')
    CANCELED = 6,  _('Отменен')
    OTHER = 7,  _('Другое')

class PAYMENT_TYPE (models.IntegerChoices):
    EMPTY = 0,  _('Не указан')
    CASH = 1,  _('Наличные')
    CARD = 2,  _('Банковская карта')
    OTHER = 3,  _('Другое')


class STAFF_ROLE (models.IntegerChoices):
    EMPTY = 0,  _('Не указана')
    CONSULTANT = 1,  _('Консультант')
    SALE_ASSISTANT = 2,  _('Продавец-консультант')
    SYSTEM_ADMINISTRATOR = 3,  _('Системный администратор')
    ADMINISTRATOR = 4,  _('Администратор')
    ACCOUNTANT = 5,  _('Кассир')

class PLACE (models.IntegerChoices):
    EMPTY = 0,  _('Не указано')
    WAREHOUSE = 1,  _('Склад')
    SHOWCASE = 2,  _('Витрина')


class Client(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    birth_date = models.DateField(blank = True, null = True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=255, blank = True, null = True, verbose_name="Моб. телефон")
    email = models.EmailField(verbose_name="Эл. почта")
    address = models.CharField(max_length=255, blank = True, null = True, verbose_name="Адрес")
    discount = models.IntegerField(choices=DISCOUNT.choices, default=DISCOUNT.EMPTY, verbose_name="Тип скидки")
    gender = models.IntegerField(choices=GENDER.choices, default=GENDER.EMPTY, verbose_name="Пол")
    job = models.CharField(max_length=255, blank = True, null = True, verbose_name="Работа/Специальность")
    description = models.TextField(blank=True, null = True, verbose_name="Описание")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    upd_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_FIO(self):
        return f"{self.first_name} {self.last_name}"

    get_FIO.short_description = _('ФИО')

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['upd_date']
        constraints = [
            UniqueConstraint(Lower('first_name'), Lower('last_name'), name='unique_lower_first_and_last_name')
        ]

class Staff(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    gender = models.IntegerField(choices=GENDER.choices, default=GENDER.EMPTY, verbose_name="Пол")
    birth_date = models.DateField(verbose_name="Дата рождения")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name="Отдел")
    role = models.IntegerField(choices=STAFF_ROLE.choices, default=STAFF_ROLE.EMPTY, verbose_name="Должность")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_FIO(self):
        return f"{self.first_name} {self.last_name}"

    get_FIO.short_description = _('ФИО')

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"
        ordering = ['first_name', 'last_name']



class Catalog(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    vendor = models.CharField(max_length=255, verbose_name="Производитель")
    vendor_code = models.CharField(max_length=255, verbose_name="Артикул")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name="Цена")

    # ИСПРАВИЛ CATEGORY с CATEGORY_ID и ДОБАВИЛ  on_delete)

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, db_index=True,
                                 verbose_name="Категория", blank = True, null = True)
    slug = AutoSlugField(populate_from=['vendor_code'], verbose_name="URL")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    last_upd_date = models.DateTimeField(auto_now=True, verbose_name="Время последнего изменения")
    warranty = models.IntegerField(choices=WARRANTY.choices, default=WARRANTY.EMPTY, verbose_name="Тип гарантии")

    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.vendor_code} {self.vendor} {self.name}"

    class Meta:
        verbose_name = "Товар в каталоге"
        verbose_name_plural = "Товары в каталоге"
        ordering = ['-last_upd_date', 'vendor', 'name']

    def get_absolute_url(self):
        return reverse('item_about', kwargs={
            'category_slug': self.category.slug,
            'item_slug':self.slug
                                             })

    def getImages(self):
        return CatalogImages.objects.filter(owner=self)

    def countAll(self):
        items = Good.objects.filter(good = self).filter(actual=True)
        count_all = 0
        count_warehouse = 0
        count_showcase = 0
        if items:
            for i in items:
                count_all += i.quantity
                if (i.place == PLACE.WAREHOUSE):
                    count_warehouse += i.quantity
                if(i.place == PLACE.SHOWCASE):
                    count_showcase+=i.quantity
        return {
            'all':count_all,
            'warehouse':count_warehouse,
            'showcase':count_showcase
        }

    def save(self, force_insert=False, force_update=False):
        self.vendor_code = self.vendor_code.lower()
        self.vendor = self.vendor.lower()
        self.name = self.name.lower()
        super(Catalog, self).save(force_insert, force_update)

class CatalogImages(models.Model):
    image = models.ImageField(upload_to="catalog_images", verbose_name="Фото", unique=True)
    owner = models.ForeignKey('Catalog', on_delete=models.CASCADE, verbose_name="Товар")
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"

    def __str__(self):
        return f"{self.image.name}"

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = AutoSlugField(populate_from='name', slugify_function=slugify, verbose_name="URL")
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null = True, blank = True, verbose_name="Родитель")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'category_slug': self.slug})

class Order(models.Model):
    buyer = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name="Покупатель")
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name="Сотрдуник")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    upd_time = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    status = models.IntegerField(choices=ORDER_STATUS.choices, default=ORDER_STATUS.INIT, verbose_name="Статус")
    payment_type = models.IntegerField(choices=PAYMENT_TYPE.choices, default=PAYMENT_TYPE.CASH, verbose_name="Тип оплаты")
    subinfo = models.TextField(null = True, blank = True, verbose_name="Дополнительная информация")

    def __str__(self):
        return f"{self.buyer} {self.add_time} "

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['upd_time']

class Good(models.Model):
    good = models.ForeignKey('Catalog', on_delete=models.CASCADE, verbose_name="Товар")
    place = models.IntegerField(choices=PLACE.choices, default=PLACE.EMPTY, verbose_name="Тип расположения")
    location_description = models.TextField(blank = True, null=True, verbose_name="Описание расположения")
    actual = models.BooleanField(default=False, verbose_name="Доступность позиции")
    quantity = models.IntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return f"[{PLACE.choices[self.place][1]}] {self.good} {self.quantity}"


    class Meta:
        verbose_name = "Товар на складе"
        verbose_name_plural = "Товары на складе"
        ordering = ['-place']

class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    parent = models.ForeignKey('Department', on_delete=models.CASCADE, blank = True, null=True, verbose_name="Родитель")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name} "

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"

class OrderGoods(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="Заказ")
    good = models.ForeignKey('Good', on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return f"{self.order} {self.good} {self.quantity}"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.good.quantity -= self.quantity
        self.good.save()
        print(self.good.quantity)
        print('HII')

    class Meta:
        verbose_name = "Заказ/Товары"
        verbose_name_plural = "Заказы/Товары"


