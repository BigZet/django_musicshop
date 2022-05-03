from django import forms
from django.forms import ModelForm

from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':"email", 'class':"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password", 'class':"form-control"}))


class CreateUserForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name',
                  'last_name',
                  'birth_date',
                  'phone',
                  'email',
                  'address',
                  'gender',
                  'description'
                  ]

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'required':"required"
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required':"required"
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required':"required"
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required':"required"
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required':"required"
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class':"form-select"
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': "form-control",
                    'style':"height: 100px"
                }
            ),

        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer',
                  'staff',
                  'payment_type',
                  'subinfo',
                  ]

        widgets = {
            'buyer': forms.Select(
                attrs={
                    'class': "form-select",
                    'id': "chooseClient"
                }
            ),
            'staff': forms.Select(
                attrs={
                    'class': "form-select",
                    'id': "chooseStaff"
                }
            ),
            'payment_type': forms.Select(
                attrs={
                    'class': "form-select",
                    'id': "paymentType"
                }
            ),
            'subinfo':forms.Textarea()
        }

    cbx_add_storage_items_first = forms.BooleanField(required=False,widget=forms.CheckboxInput( attrs={
        'type' : "checkbox",
        'class' :"form-check-input",
        'id':"cbx_first_storage"
    }))

    def save(self, cart = {}, commit=True):
        items_to_add = []
        place_prior = [PLACE.WAREHOUSE, PLACE.SHOWCASE][self.cleaned_data['cbx_add_storage_items_first']]
        place_second = [PLACE.WAREHOUSE, PLACE.SHOWCASE][not self.cleaned_data['cbx_add_storage_items_first']]
        for item_id in cart:
            items_goods = Good.objects.filter(good_id=item_id)
            require_quantity = cart[item_id]
            if len(items_goods)>1:
                prior_item = items_goods.get(place=place_prior)
                if prior_item.quantity < require_quantity:
                    require_quantity -= prior_item.quantity
                    items_to_add.append([prior_item, prior_item.quantity])

                    second_item = items_goods.get(place=place_second)
                    items_to_add.append([second_item, require_quantity])
                else:
                    items_to_add.append([prior_item, require_quantity])
            elif len(items_goods)==1:
                prior_item = items_goods[0]
                items_to_add.append([prior_item, require_quantity])

        print(items_to_add)
        order = super(OrderForm, self).save(commit=commit)
        for i in items_to_add:
            OrderGoods.objects.create(order=order, good=i[0], quantity=i[1])

        return order


