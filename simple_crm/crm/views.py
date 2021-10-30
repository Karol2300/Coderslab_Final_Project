# Clients list per investment
#investment details
# Products list per investment
# Product list per city,district
# sales by city, sales by district
# transactions detail by investment (avg price, deal time span, )
from crm.models import Client, SalesPerson
from django.views import View
from django.http import request
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rep.models import InvestmentProject, Product, PricingPlan

from crm.forms import ClientForm_1,ClientForm_2, SalesPersonForm_1, SalesPersonForm_2, PickClientForm


# from clcrypto import generate_salt,check_password,hash_password






class AddClient(View):
        def get(self, request):
            if request.method == 'GET':
                form_1 = ClientForm_1
                form_2 = ClientForm_2

                return render(request,'AddClient.html', {'form_1': form_1,
                                                          'form_2': form_2,})
        def post(self,request):
            if request.method == "POST":
                form_1 = ClientForm_1(request.POST)
                form_2 = ClientForm_2(request.POST)
                if form_1.is_valid() and form_2.is_valid():
                    new_client = Client.objects.create(first_name = form_1.cleaned_data['first_name'], last_name = form_1.cleaned_data['last_name'],
                                       city = form_1.cleaned_data['city'], address = form_1.cleaned_data['address'], post_code = form_1.cleaned_data['post_code'],
                                       phone_number = form_1.cleaned_data['phone_number'], email = form_1.cleaned_data['email'],
                                       preferred_contact_type = form_1.cleaned_data['preferred_contact_type'],
                                       additional_info = form_1.cleaned_data['additional_info'])

                    new_client.investments.set(form_2.cleaned_data['investments'])
                    new_client.products.set(form_2.cleaned_data['products'])

                    message = f"Client added successfully"
                    return render(request, 'AddClient.html', {'form_1': form_1,'form_2': form_2, 'message': message})
                else:
                    message = f"Incorrect data!"
                    return render(request, 'AddClient.html', {'form_1': form_1,'form_2': form_2, 'message': message})



class AddSalesPerson(View):

        def get(self, request):
            if request.method == 'GET':
                form_1 = SalesPersonForm_1
                form_2 = SalesPersonForm_2
                return render(request,'AddSalesperson.html', {'form_1': form_1,
                                                          'form_2': form_2,})
        def post(self,request):
            if request.method == "POST":
                form_1 = SalesPersonForm_1(request.POST)
                form_2 = SalesPersonForm_2(request.POST)
                if form_1.is_valid() and form_2.is_valid():
                    new_salesperson = SalesPerson.objects.create(first_name = form_1.cleaned_data['first_name'], last_name = form_1.cleaned_data['last_name'],
                                       login = form_1.cleaned_data['login'], password = form_1.cleaned_data['password'],)

                    new_salesperson.investments.set(form_2.cleaned_data['investments'])
                    new_salesperson.products.set(form_2.cleaned_data['products'])
                    new_salesperson.clients.set(form_2.cleaned_data['clients'])
                    message = f"Sales person added successfully"
                    return render(request, 'AddSalesperson.html', {'form_1': form_1,'form_2': form_2, 'message': message})
                else:
                    message = f"Incorrect data!"
                    return render(request, 'AddSalesperson.html', {'form_1': form_1,'form_2': form_2, 'message': message})


class ShowClient(View):
    def get(self, request):
        if request.method == 'GET':
            form = PickClientForm

            return render(request, 'ShowClient.html', {'form': form})

    def post(self, request):
        if request.method == "POST":
            form_1 = PickClientForm(request.POST)
            if form_1.is_valid():
                client = Client.objects.get(pk=form_1.cleaned_data['id'])
                ctx = {'client': client, }
                return render(request, 'ShowClient.html', ctx)
            else:
                message = f"Incorrect Client!"




