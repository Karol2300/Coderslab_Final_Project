from django.forms import ModelForm, Form
from crm.models import Client, SalesPerson
from django import forms
from crm.models import contact_type
from django.forms import HiddenInput


class ClientForm_1(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    post_code = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    preferred_contact_type = forms.ChoiceField(choices=contact_type)
    additional_info = forms.CharField(widget=forms.Textarea)


class ClientForm_2(ModelForm):
    class Meta:
        model = Client
        fields = ['investments', 'products']


class SalesPersonForm_1(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    login = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class SalesPersonForm_2(ModelForm):
    class Meta:
        model = SalesPerson
        fields = ['investments', 'products', 'clients']

class PickClientForm(forms.Form):
    names = Client.objects.values_list('first_name','last_name','id')
    name = forms.ModelChoiceField(widget=forms.Select, queryset=names)


