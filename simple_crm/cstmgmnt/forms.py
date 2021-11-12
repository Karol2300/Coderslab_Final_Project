from django.forms import ModelForm, Form
from cstmgmnt.models import Client, SalesPerson, InvestmentProject
from django import forms
from cstmgmnt.models import contact_type
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


class SalesPersonForm_2(ModelForm):
    class Meta:
        model = SalesPerson
        fields = ['investments', 'products', 'clients', 'users']


class PickInvestment(forms.Form):
    investment = forms.ModelChoiceField(widget=forms.Select, queryset=InvestmentProject.objects.all())


class PickClient(forms.Form):
    name = forms.ModelChoiceField(widget=forms.Select, queryset=Client.objects.all())


class EditClientForm_1(ModelForm):
    id = forms.CharField(max_length=255)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'city', 'address', 'post_code', 'phone_number', 'email',
                  'preferred_contact_type', 'additional_info']


class PickSalesperson(forms.Form):
    salesperson = forms.ModelChoiceField(widget=forms.Select, queryset=SalesPerson.objects.all())


class EditSalesPersonForm_1(ModelForm):
    # id = forms.CharField(max_length=255)
    class Meta:
        model = SalesPerson
        fields = ['first_name', 'last_name']


