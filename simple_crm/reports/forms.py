from django.forms import ModelForm
from django import forms
from django.forms import PasswordInput
from reports.models import Product, InvestmentProject, PricingPlan, available_floor, available_rooms, direction, \
    district, \
    overall_apartment_score, product_status
from django.contrib.auth.models import User

apartment_type = [
    ('0-30', '0-30'),
    ('30-40', '30-40'),
    ('40-55', '40-55'),
    ('55-75', '55-75'),
    ('75-100', '75-100'),
    ('100-140', '100-140'),
]

class ProductForm_1(forms.Form):
    code = forms.CharField(max_length=255)
    area = forms.DecimalField(max_digits=10, decimal_places=2)
    direction = forms.ChoiceField(choices=direction)
    floor = forms.ChoiceField(choices=available_floor)
    number_of_rooms = forms.ChoiceField(choices=available_rooms)
    rating = forms.ChoiceField(choices=overall_apartment_score, required=False)
    balcony = forms.BooleanField(required=False)
    loggia = forms.BooleanField(required=False)
    status = forms.ChoiceField(choices=product_status)
    price = forms.DecimalField(max_digits=10, decimal_places=2)


class EditProductForm_1(ModelForm):
    id = forms.CharField(max_length=255)

    class Meta:
        model = Product
        fields = ['code', 'direction', 'floor', 'number_of_rooms', 'rating', 'balcony', 'loggia', 'status', 'price']


class ProductForm_2(ModelForm):
    class Meta:
        model = Product
        fields = ['investments']


class InvestmentForm(forms.Form):
    name = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    district = forms.ChoiceField(choices=district)
    specification = forms.CharField(widget=forms.Textarea)
    number_of_apartments = forms.IntegerField()
    start_date = forms.DateTimeField()
    finnish_date = forms.DateTimeField()


class PricingPlanForm_1(forms.Form):
    pricing_plan_name = forms.CharField(max_length=255)
    pricing_plan_code = forms.CharField(max_length=255)
    is_active = forms.BooleanField(required=False)
    nett_price = forms.DecimalField(max_digits=10, decimal_places=2)
    gross_price = forms.DecimalField(max_digits=10, decimal_places=2)
    nett_price_per_sqm = forms.DecimalField(max_digits=10, decimal_places=2)
    gross_price_per_sqm = forms.DecimalField(max_digits=10, decimal_places=2)


class PricingPlanForm_2(ModelForm):
    class Meta:
        model = PricingPlan
        fields = ['products']


class EditInvestmentForm(ModelForm):
    class Meta:
        model = InvestmentProject
        fields = ['name', 'city', 'address', 'district', 'specification', 'number_of_apartments', 'start_date',
                  'finnish_date']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserFormPassword(forms.Form):
    password = forms.CharField(max_length=255, widget=PasswordInput)


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class SalesFilterForm(forms.Form):
    area_range = forms.ChoiceField(choices=apartment_type)
    status = forms.ChoiceField(choices=product_status)
    number_of_rooms = forms.ChoiceField(choices=available_rooms)
    floor = forms.ChoiceField(choices=available_floor)


# class SalesFilterAreaForm(forms.Form):
#     area_range = forms.ChoiceField()
#
# class SalesFilterStatusForm(forms.Form):
#     status = forms.ChoiceField()
#
# class SalesFilterRoomsForm(forms.Form):
#     number_of_rooms = forms.ChoiceField()
#
# class SalesFilterFloorForm(forms.Form):
#     floor = forms.ChoiceField()

# class SalesFilterAreaForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['area']
#         # area_range = forms.ChoiceField()
#
# class SalesFilterStatusForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['status']
#
# class SalesFilterRoomsForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['number_of_rooms']
#
# class SalesFilterFloorForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['floor']