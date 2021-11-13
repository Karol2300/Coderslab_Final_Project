# Clients list per investment
# investment details
# Products list per investment
# Product list per city,district
# sales by city, sales by district
# transactions detail by investment (avg price, deal time span, )
from cstmgmnt.models import Client, SalesPerson
from django.views import View
from django.http import request
from django import forms
from django.forms import ModelForm, Form
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from reports.models import InvestmentProject, Product, PricingPlan
from django.forms import model_to_dict
from django.contrib.auth.models import User, Permission
from django.contrib.auth import logout

from cstmgmnt.forms import ClientForm_1, ClientForm_2, SalesPersonForm_1, SalesPersonForm_2, PickInvestment, PickClient, \
    EditClientForm_1, EditSalesPersonForm_1, PickSalesperson
from reports.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class AddClient(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
        result : add client to client table,
        requirements_1 : user must be logged in (LoginRequiredMixin),
        requirements_2: user must have permission"""

    permission_required = ('cstmgmnt.add_client')

    def get(self, request):
        """class  method,
            result : show add client forms,
            requirements: user must have permission"""

        form_1 = ClientForm_1
        form_2 = ClientForm_2
        if request.method == 'GET' and request.user.has_perm('cstmgmnt.add_client'):

            return render(request, 'AddClient.html', {'form_1': form_1,
                                                      'form_2': form_2, })
        else:
            message = f"Authentication required or incorrect permission, contact admin"
            return render(request, 'AddClient.html', {
                'message': message})

    def post(self, request):
        """class  method,
            result : add client to client list,
            requirements: user must have permission"""

        form_1 = ClientForm_1(request.POST)
        form_2 = ClientForm_2(request.POST)

        if request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')

        elif request.method == "POST" and 'add_client' in request.POST and request.user.has_perm('cstmgmnt.add_client'):
            if form_1.is_valid() and form_2.is_valid():
                new_client = Client.objects.create(first_name=form_1.cleaned_data['first_name'],
                                                   last_name=form_1.cleaned_data['last_name'],
                                                   city=form_1.cleaned_data['city'],
                                                   address=form_1.cleaned_data['address'],
                                                   post_code=form_1.cleaned_data['post_code'],
                                                   phone_number=form_1.cleaned_data['phone_number'],
                                                   email=form_1.cleaned_data['email'],
                                                   preferred_contact_type=form_1.cleaned_data['preferred_contact_type'],
                                                   additional_info=form_1.cleaned_data['additional_info'])
                new_client.investments.set(form_2.cleaned_data['investments'])
                new_client.products.set(form_2.cleaned_data['products'])
                # new_client.users.set(form_2.cleaned_data['users'])
                message = f"Client added successfully"
                return render(request, 'AddClient.html', {'form_1': form_1, 'form_2': form_2, 'message': message, })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddClient.html', {'form_1': form_1, 'form_2': form_2, 'message': message})



        else:
            message = f"Incorrect data!"
            return render(request, 'AddClient.html', {'form_1': form_1, 'form_2': form_2, 'message': message})


class ShowClient(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
            result : clients list per investment project,
            requirements_1 : user must be logged in (LoginRequiredMixin),
            requirements_2: user mus have permission
              """
    permission_required = ('cstmgmnt.view_client', 'cstmgmnt.change_client')

    def get(self, request):
        """class  method,
            result : show pick investment form,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('cstmgmnt.view_client') and \
                request.user.has_perm('cstmgmnt.change_client'):
            client_by_investment_form = PickInvestment()
            return render(request, 'ShowClient_pick_investment.html',
                          {'client_by_investment_form': client_by_investment_form, })

    def post(self, request):
        """class  method,
            result : show list of clients per investment, generate links to edit/delete client,
            requirements: user must have permission"""

        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST and \
                request.user.has_perm('cstmgmnt.view_client') and request.user.has_perm('cstmgmnt.change_client'):
            data = PickInvestment(request.POST)
            if data.is_valid():
                if len(Client.objects.all().filter(
                        investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id))) > 0:
                    client = Client.objects.all().filter(
                        investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).order_by('last_name')
                    clients = [val for val in client]
                    return render(request, 'ShowClient.html', {'clients': clients, })
                else:
                    message = "There are no clients for chosen investment project !"
                    return render(request, 'ShowClient.html', {'message': message})

            else:
                message = "Incorrect Client !"
                return render(request, 'ShowClient.html', {'message': message})

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')

        else:
            message = "Incorrect Client!"
            client_by_investment_form = PickInvestment()
            return render(request, 'ShowClient_pick_investment.html',
                          {'client_by_investment_form': client_by_investment_form,
                           'message': message})


class ShowClientData(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
       result : client details, edit client, delete client
       requirements_1 : user must be logged in (LoginRequiredMixin),
       requirements_2: user mus have permission
    """
    permission_required = (
    'cstmgmnt.change_client', 'cstmgmnt.view_client', 'cstmgmnt.delete_client', 'cstmgmnt.add_client')

    def get(self, request, *args, **kwargs):
        """class  method,
        result : show list of clients per investment, generate links to edit/delete client,
        requirements: user must have permission"""

        if request.method == 'GET' and kwargs['client_id'] and request.user.has_perm(
                'cstmgmnt.view_client') and request.user.has_perm('cstmgmnt.change_client') and request.user.has_perm(
                'cstmgmnt.delete_client') and request.user.has_perm('cstmgmnt.add_client'):
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
        """class  method,
                result : show client details form, edit client ,delete client,
                requirements: user must have permission"""

        if request.method == "POST" and EditClientForm_1(request.POST) and ClientForm_2(request.POST) \
                and 'save_client_data' in request.POST and request.user.has_perm(
            'cstmgmnt.view_client') and request.user.has_perm('cstmgmnt.change_client') and request.user.has_perm(
            'cstmgmnt.delete_client') and request.user.has_perm('cstmgmnt.add_client'):
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
                client = Client.objects.get(pk=str(client_id))
                form_client_basic_data = EditClientForm_1(initial=model_to_dict(client))
                form_client_rel_data = ClientForm_2(initial=model_to_dict(client))
                return render(request, 'ShowClientDetails.html', {'message': message,
                                                                  'form_client_basic_data': form_client_basic_data,
                                                                  'form_client_rel_data': form_client_rel_data, })
            else:
                message = "Incorrect data!"
                client = Client.objects.get(pk=str(client_id))
                form_client_basic_data = EditClientForm_1(initial=model_to_dict(client))
                form_client_rel_data = ClientForm_2(initial=model_to_dict(client))
                return render(request, 'ShowClientDetails.html', {'message': message,
                                                                  'form_client_basic_data': form_client_basic_data,
                                                                  'form_client_rel_data': form_client_rel_data, })

        if request.method == "POST" and EditClientForm_1(request.POST) and ClientForm_2(request.POST) \
                and 'delete_client' in request.POST and request.user.has_perm(
            'cstmgmnt.view_client') and request.user.has_perm('cstmgmnt.change_client'):
            client_id = kwargs['client_id']
            client = Client.objects.get(pk=str(client_id))
            client.delete()
            message = "Client removed from data base!"
            return render(request, 'ShowClientDetails.html', {'message': message, })

        if request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class AddSalesPerson(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
           result : add salesperson to salesperson
           requirements_1 : user must be logged in (LoginRequiredMixin),
           requirements_2: user mus have permission
        """
    permission_required = ('cstmgmnt.change_salesperson', 'cstmgmnt.view_salesperson', 'cstmgmnt.add_salesperson',
                           'cstmgmnt.delete_salesperson')

    def get(self, request):
        """class  method,
            result : show add client forms,
            requirements: user must have permission"""
        if request.method == 'GET' and request.user.has_perm('cstmgmnt.change_salesperson') and request.user.has_perm(
                'cstmgmnt.add_salesperson'):
            form_1 = SalesPersonForm_1()
            form_2 = SalesPersonForm_2()
            return render(request, 'AddSalesperson.html', {'form_1': form_1,
                                                           'form_2': form_2, })

    def post(self, request):
        """class  method,
           result : add client to clients list,
           requirements: user must have permission"""

        if request.method == "POST" and 'add_salesperson' in request.POST and request.user.has_perm(
                'cstmgmnt.add_salesperson') and request.user.has_perm('cstmgmnt.change_salesperson'):
            form_1 = SalesPersonForm_1(request.POST)
            form_2 = SalesPersonForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                new_salesperson = SalesPerson.objects.create(first_name=form_1.cleaned_data['first_name'],
                                                             last_name=form_1.cleaned_data['last_name'],
                                                             users=form_2.cleaned_data['users'])

                new_salesperson.investments.set(form_2.cleaned_data['investments'])
                new_salesperson.products.set(form_2.cleaned_data['products'])
                new_salesperson.clients.set(form_2.cleaned_data['clients'])

                new_salesperson.save()
                message = f"Sales person added successfully"
                return render(request, 'AddSalesperson.html',
                              {'form_1': form_1, 'form_2': form_2, 'message': message,
                               })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddSalesperson.html',
                              {'form_1': form_1, 'form_2': form_2, 'message': message, })

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowSalesPerson(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
       result : show salesperson list
       requirements_1 : user must be logged in (LoginRequiredMixin),
       requirements_2: user mus have permission"""

    permission_required = ('cstmgmnt.change_salesperson', 'cstmgmnt.view_salesperson')

    def get(self, request):
        """class  method,
            result : show pick investment form,
            requirements: user must have permission"""
        if request.method == 'GET' and request.user.has_perm(permission_required):
            salesperson_form = PickInvestment()
            return render(request, 'ShowSalesperson_pick_investment.html', {'salesperson_form': salesperson_form, })

    def post(self, request):
        """class  method,
            result : show salesperson list per investment,
            requirements: user must have permission"""
        if request.method == "POST" and PickInvestment(request.POST) and 'salesperson_form' in request.POST and \
                request.user.has_perm('cstmgmnt.change_salesperson') and request.user.has_perm(
            'cstmgmnt.view_salesperson'):
            data = PickInvestment(request.POST)
            if data.is_valid():
                salespersons = SalesPerson.objects.all().filter(investments=
                                                                InvestmentProject.objects.get(
                                                                    pk=data.cleaned_data['investment'].id)).order_by('last_name')
                salespersons_ls = [val for val in salespersons]
                return render(request, 'ShowSalesperson.html', {'salespersons': salespersons_ls, })
            else:
                message = f"Incorrect Client!"
                return render(request, 'ShowSalesperson.html', {'message': message})

        if request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowSalesPersonData(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
      result : show salesperson details, edit salesperson, delete_salesperson,
      requirements_1 : user must be logged in (LoginRequiredMixin),
      requirements_2: user mus have permission"""

    permission_required = ('cstmgmnt.change_salesperson', 'cstmgmnt.view_salesperson', 'cstmgmnt.edit_salesperson',
                           'cstmgmnt.delete_salesperson')

    def get(self, request, *args, **kwargs):
        """class  method,
            result : show salesperson data form,
            requirements: user must have permission"""

        if request.method == 'GET' and kwargs['salesperson_id'] and request.user.has_perm('cstmgmnt.change_salesperson') \
                and request.user.has_perm('cstmgmnt.view_salesperson'):
            salesperson_id = kwargs['salesperson_id']
            salesperson = SalesPerson.objects.get(pk=salesperson_id)
            form_salesperson_basic_data = EditSalesPersonForm_1(initial=model_to_dict(salesperson))
            form_salesperson_rel_data = SalesPersonForm_2(initial=model_to_dict(salesperson))
            return render(request, 'ShowSalespersonDetails.html',
                          {'form_salesperson_basic_data': form_salesperson_basic_data,
                           'form_salesperson_rel_data': form_salesperson_rel_data, })
        else:
            message = f"Salesperson not found!"
            return render(request, 'ShowSalespersonDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        """class  method,
            result : show salesperson details form, edit client ,delete client,
            requirements: user must have permission"""

        if request.method == "POST" and EditSalesPersonForm_1(request.POST) and SalesPersonForm_2(request.POST) \
                and 'save_salesperson_data' in request.POST and request.user.has_perm('cstmgmnt.change_salesperson') \
                and request.user.has_perm('cstmgmnt.add_salesperson') \
                and request.user.has_perm('cstmgmnt.view_salesperson'):
            salesperson_id = kwargs['salesperson_id']
            form_1 = EditSalesPersonForm_1(request.POST)
            if form_1.is_valid():
                update_salesperson = SalesPerson.objects.get(pk=salesperson_id)
                form_1 = EditSalesPersonForm_1(request.POST, instance=update_salesperson)
                form_2 = SalesPersonForm_2(request.POST, instance=update_salesperson)
                form_1.save()
                form_2.save()
                message = "Salesperson data updated"
                form_salesperson_basic_data = EditSalesPersonForm_1(initial=model_to_dict(update_salesperson))
                form_salesperson_rel_data = SalesPersonForm_2(initial=model_to_dict(update_salesperson))
                return render(request, 'ShowSalespersonDetails.html', {'message': message,
                                                           'form_salesperson_basic_data': form_salesperson_basic_data,
                                                           'form_salesperson_rel_data': form_salesperson_rel_data, })
            else:
                message = "Incorrect !"
                update_salesperson = SalesPerson.objects.get(pk=str(salesperson_id))
                form_salesperson_basic_data = EditSalesPersonForm_1(initial=model_to_dict(update_salesperson))
                form_salesperson_rel_data = SalesPersonForm_2(initial=model_to_dict(update_salesperson))
                return render(request, 'ShowSalespersonDetails.html', {'message': message,
                                                           'form_salesperson_basic_data': form_salesperson_basic_data,
                                                           'form_salesperson_rel_data': form_salesperson_rel_data, })

        elif request.method == 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')

        elif request.method == "POST" and EditSalesPersonForm_1(request.POST) and SalesPersonForm_2(request.POST) \
                and 'delete_salesperson' in request.POST and request.user.has_perm('cstmgmnt.change_salesperson') \
                and request.user.has_perm('cstmgmnt.add_salesperson') \
                and request.user.has_perm('cstmgmnt.view_salesperson') and \
                request.user.has_perm('cstmgmnt.delete_salesperson'):
            salesperson_id = kwargs['salesperson_id']
            salesperson = SalesPerson.objects.get(pk=str(salesperson_id))
            salesperson.delete()
            message = "Salesperson removed from data base!"
            return render(request, 'ShowSalespersonDetails.html', {'message': message, })

        else:
            salesperson_id = kwargs['salesperson_id']
            message = "Incorrect data!"
            salesperson = SalesPerson.objects.get(pk=str(salesperson_id))
            form_salesperson_basic_data = EditSalesPersonForm_1(initial=model_to_dict(salesperson))
            form_salesperson_rel_data = SalesPersonForm_2(initial=model_to_dict(salesperson))
            return render(request, 'ShowSalespersonDetails.html', {'message': message,
                                                           'form_salesperson_basic_data': form_salesperson_basic_data,
                                                           'form_salesperson_rel_data': form_salesperson_rel_data, })


class ValidateUser(View):
    """class based view,
      result : validate user"""

    def get(self, request):
        """ class method
            result : show validation form"""

        if request.method == "GET":
            return render(request, 'Login.html', {'login_form': LoginForm})

    def post(self, request):
        """ class method
            result : show validation result"""

        if request.method == "POST":
            form = LoginForm(request.POST)
            username = form['username'].value()
            password = form['password'].value()
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                user = request.user
                if user.is_authenticated:
                    return redirect('/MainMenu/')

            elif request.method == "POST" and 'logout' in request.POST:
                logout(request)
                return redirect('/loginPage/')

            else:
                message = 'Niepoprawny login/hasło'
                return render(request, 'Login.html', {'login_form': LoginForm(), 'message': message})


