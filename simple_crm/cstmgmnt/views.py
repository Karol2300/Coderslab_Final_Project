# Clients list per investment
#investment details
# Products list per investment
# Product list per city,district
# sales by city, sales by district
# transactions detail by investment (avg price, deal time span, )
from cstmgmnt.models import Client, SalesPerson
from django.views import View
from django.http import request
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from reports.models import InvestmentProject, Product, PricingPlan
from django.forms import model_to_dict
from django.contrib.auth.models import User

from cstmgmnt.forms import ClientForm_1, ClientForm_2, SalesPersonForm_1, SalesPersonForm_2, PickInvestment, PickClient, \
    EditClientForm_1, EditSalesPersonForm_1, PickSalesperson





class AddClient(View):
        def get(self, request):
            if request.method == 'GET':
                form_1 = ClientForm_1
                form_2 = ClientForm_2

                return render(request,'AddClient.html', {'form_1': form_1,
                                                          'form_2': form_2,})
        def post(self,request):
            if request.method == "POST":
                form_1 = ClientForm_1(request.POST or None)
                form_2 = ClientForm_2(request.POST or None)
                if form_1.is_valid() and form_2.is_valid():
                    new_client = Client.objects.create(first_name = form_1.cleaned_data['first_name'], last_name = form_1.cleaned_data['last_name'],
                                       city = form_1.cleaned_data['city'], address = form_1.cleaned_data['address'], post_code = form_1.cleaned_data['post_code'],
                                       phone_number = form_1.cleaned_data['phone_number'], email = form_1.cleaned_data['email'],
                                       preferred_contact_type = form_1.cleaned_data['preferred_contact_type'],
                                       additional_info = form_1.cleaned_data['additional_info'])

                    new_client.investments.set(form_2.cleaned_data['investments'])
                    new_client.products.set(form_2.cleaned_data['products'])
                    new_client.users.set(form_2.cleaned_data['users'])
                    message = f"Client added successfully"
                    return render(request, 'AddClient.html', {'form_1': form_1,'form_2': form_2, 'message': message,})
                else:
                    message = f"Incorrect data!"
                    return render(request, 'AddClient.html', {'form_1': form_1,'form_2': form_2, 'message': message})




class ShowClient(View):

    def get(self, request):
        if request.method == 'GET':
            client_by_investment_form = PickInvestment()
            return render(request, 'ShowClient_pick_investment.html', {'client_by_investment_form': client_by_investment_form,})

    def post(self, request):
        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST:
            data = PickInvestment(request.POST)
            if data.is_valid():
                client = Client.objects.all().filter(investments = InvestmentProject.objects.get(id=data.cleaned_data['investment'].id))
                clients = [val for val in client]
                return render(request, 'ShowClient.html', {'clients': clients,})
            else:
                message = f"Incorrect Client!"
                return render(request, 'ShowClient.html', {'message': message})

class ShowClientData(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and kwargs['client_id']:
            client_id = kwargs['client_id']
            client = Client.objects.get(pk=str(client_id))
            form_client_basic_data = EditClientForm_1(initial=model_to_dict(client))
            form_client_rel_data = ClientForm_2(initial=model_to_dict(client))
            return render(request, 'ShowClientDetails.html', {'form_client_basic_data': form_client_basic_data,
                                                               'form_client_rel_data': form_client_rel_data, })
        else:
            message = f"Client not found!"
            return render(request, 'ShowClient.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and EditClientForm_1(request.POST) and ClientForm_2(request.POST) \
                and 'save_client_data' in request.POST:
            client_id = kwargs['client_id']
            form_1 = EditClientForm_1(request.POST)
            form_2 = ClientForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                update_client = Client.objects.get(pk=form_1.cleaned_data['id'])
                form_1 = EditClientForm_1(request.POST, instance=update_client)
                form_2 = ClientForm_2(request.POST, instance=update_client)
                form_1.save()
                form_2.save()
                message = "Client data updated"
                return render(request, 'ShowClientDetails.html', {'message': message})
            else:
                message = "Incorrect data!"
                client = Client.objects.get(pk=str(client_id))
                form_client_basic_data = EditClientForm_1(initial=model_to_dict(client))
                form_client_rel_data = ClientForm_2(initial=model_to_dict(client))
                return render(request, 'ShowClientDetails.html', {'message': message,
                                                           'form_client_basic_data': form_client_basic_data,
                                                            'form_client_rel_data': form_client_rel_data, })

        if request.method == "POST" and EditClientForm_1(request.POST) and ClientForm_2(request.POST) \
                and 'delete_client' in request.POST:
            client_id = kwargs['client_id']
            client = Client.objects.get(pk=str(client_id))
            client.delete()
            message = "Client removed from data base!"
            return render(request, 'ShowClientDetails.html', {'message': message,})

class AddSalesPerson(View):

    def get(self, request):
        if request.method == 'GET':
            form_1 = SalesPersonForm_1()
            form_2 = SalesPersonForm_2()
            return render(request, 'AddSalesperson.html', {'form_1': form_1,
                                                           'form_2': form_2, })

    def post(self, request):
        if request.method == "POST":
            form_1 = SalesPersonForm_1(request.POST)
            form_2 = SalesPersonForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                new_salesperson = SalesPerson.objects.create(first_name=form_1.cleaned_data['first_name'],
                                                             last_name=form_1.cleaned_data['last_name'],)
                                                             # login=form_1.cleaned_data['login'],
                                                             # password=form_1.cleaned_data['password'], )

                new_salesperson.investments.set(form_2.cleaned_data['investments'])
                new_salesperson.products.set(form_2.cleaned_data['products'])
                new_salesperson.clients.set(form_2.cleaned_data['clients'])
                message = f"Sales person added successfully"
                return render(request, 'AddSalesperson.html',
                              {'form_1': form_1, 'form_2': form_2, 'message': message,
                               })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddSalesperson.html',
                              {'form_1': form_1, 'form_2': form_2, 'message': message,
                               })


class ShowSalesPerson(View):
    def get(self, request):
        if request.method == 'GET':
            salesperson_form = PickInvestment()
            return render(request, 'ShowSalesperson_pick_investment.html', {'salesperson_form': salesperson_form,})

    def post(self, request):
        if request.method == "POST" and PickInvestment(request.POST) and 'salesperson_form' in request.POST:
            data = PickInvestment(request.POST)
            if data.is_valid():
                salespersons = SalesPerson.objects.all().filter(investments =
                                    InvestmentProject.objects.get(pk=data.cleaned_data['investment'].id))

                salespersons_ls = [val for val in salespersons]
                return render(request, 'ShowSalesperson.html', {'salespersons': salespersons_ls,})
            else:
                message = f"Incorrect Client!"
                return render(request, 'ShowSalesperson.html', {'message': message})


class ShowSalesPersonData(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and kwargs['salesperson_id']:
            salesperson_id = kwargs['salesperson_id']
            salesperson = SalesPerson.objects.get(pk=salesperson_id)
            form_salesperson_basic_data = EditSalesPersonForm_1(initial=model_to_dict(salesperson))
            form_salesperson_rel_data = SalesPersonForm_2(initial=model_to_dict(salesperson))
            return render(request, 'ShowSalespersonDetails.html', {'form_salesperson_basic_data': form_salesperson_basic_data,
                                                               'form_salesperson_rel_data': form_salesperson_rel_data, })
        else:
            message = f"Salesperson not found!"
            return render(request, 'ShowSalespersonDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and EditSalesPersonForm_1(request.POST) and SalesPersonForm_2(request.POST) \
                and 'save_salesperson_data' in request.POST:
            salesperson_id = kwargs['salesperson_id']
            form_1 = EditSalesPersonForm_1(request.POST)
            form_2 = SalesPersonForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                update_salesperson = SalesPerson.objects.get(pk=form_1.cleaned_data['id'])
                form_1 = EditSalesPersonForm_1(request.POST, instance=update_salesperson)
                form_2 = SalesPersonForm_2(request.POST, instance=update_salesperson)
                form_1.save()
                form_2.save()
                message = "Salesperson data updated"
                return render(request, 'ShowSalespersonDetails.html', {'message': message})
            else:
                message = "Incorrect data!"
                salesperson = SalesPerson.objects.get(pk=str(salesperson_id))
                form_salesperson_basic_data = EditSalesPersonForm_1(initial=model_to_dict(salesperson))
                form_salesperson_rel_data = SalesPersonForm_2(initial=model_to_dict(salesperson))
                return render(request, 'ShowSalespersonDetails.html', {'message': message,
                                                           'form_salesperson_basic_data': form_salesperson_basic_data,
                                                            'form_salesperson_rel_data': form_salesperson_rel_data, })

