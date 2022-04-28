from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.


class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        output = []

        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" alt="{file_name}" width="400" height="200" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('get_FIO', 'phone', 'email', 'birth_date',)
    search_fields = ('first_name','last_name', 'phone', 'email',)
    list_filter = ('gender', 'discount', 'upd_date',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('get_FIO', 'role', 'department',)
    search_fields = ('first_name', 'last_name',)
    list_filter = ('role', 'department', 'gender',)


class OrderItemsAdmin(admin.TabularInline):
    model = OrderGoods
    min_num = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('upd_time',  'buyer', 'status', 'staff',  'payment_type', )
    search_fields = ('buyer', 'staff',)
    list_filter = ('status', 'payment_type', )
    inlines = [OrderItemsAdmin]

class CatalogImageAdmin(admin.StackedInline):
    model = CatalogImages

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }





@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'category', 'vendor_code', 'warranty', 'slug')
    search_fields = ('name', 'vendor', 'vendor_code',)
    list_filter = ('vendor', 'category', 'warranty',)
    inlines = [CatalogImageAdmin]



    class Meta:
        model = Catalog




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('good', 'place', 'actual', 'quantity',)
    list_editable = ('actual', 'quantity',)
    list_filter = ('place', 'actual',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Client, ClientAdmin)
# admin.site.register(Staff, StaffAdmin)
# #admin.site.register(Catalog, CatalogAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(Good, GoodAdmin)
# admin.site.register(Department)
# admin.site.register(Cart, CartAdmin)
# #admin.site.register(CatalogImages)