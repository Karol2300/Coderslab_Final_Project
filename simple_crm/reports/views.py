
from django.shortcuts import render
from reports.forms import ProductForm_1, ProductForm_2, InvestmentForm, PricingPlanForm_1, PricingPlanForm_2, \
    EditProductForm_1, EditInvestmentForm, UserForm, UserFormPassword, SalesFilterForm

from django.views import View
from reports.models import Product, PricingPlan, InvestmentProject
from cstmgmnt.models import Client
from cstmgmnt.forms import PickInvestment, PickClient
from django.forms import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect


import os


# from matplotlib.backends.backend_agg import FigureCanvasAgg





class AddProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
    result : add product to project investment,
    requirements_1 : user must be logged in (LoginRequiredMixin),
    requirements_2: user mus have permission
      """
    permission_required = (
        'reports.add_product', 'reports.view_product', 'reports.delete_product', 'reports.change_product',)

    def get(self, request):
        """class  method,
            result : show add product forms,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('reports.add_product') and \
                request.user.has_perm('reports.view_product'):
            form_1 = ProductForm_1
            form_2 = ProductForm_2

            return render(request, 'AddProduct.html', {'form_1': form_1,
                                                       'form_2': form_2, })

    def post(self, request):
        """class  method,
            result : show add product result,
            requirements: user must have permission"""

        if request.method == "POST" and 'add_product' in request.POST \
                and request.user.has_perm('reports.add_product') and request.user.has_perm('reports.view_product'):
            form_1 = ProductForm_1(request.POST)
            form_2 = ProductForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                try:
                    new_product = Product.objects.create(code=form_1.cleaned_data['code'],
                                                         area=form_1.cleaned_data['area'],
                                                         direction=form_1.cleaned_data['direction'],
                                                         floor=form_1.cleaned_data['floor'],
                                                         number_of_rooms=form_1.cleaned_data['number_of_rooms'],
                                                         rating=form_1.cleaned_data['rating'],
                                                         balcony=form_1.cleaned_data['balcony'],
                                                         loggia=form_1.cleaned_data['loggia'],
                                                         status=form_1.cleaned_data['status'],
                                                         price=form_1.cleaned_data['price'],
                                                         investments=form_2.cleaned_data['investments'])
                    # new_product['investments'].set(form_2.cleaned_data['investments'].id)
                    new_product.save()
                    message = f"Product added successfully"
                    return render(request, 'AddProduct.html',
                                  {'form_1': form_1, 'form_2': form_2, 'message': message, })
                except:
                    message = f"Incorrect data!"
                    return render(request, 'AddProduct.html', {'form_1': form_1, 'form_2': form_2, 'message': message})

            else:
                message = f"Incorrect data!"
                return render(request, 'AddProduct.html', {'form_1': form_1, 'form_2': form_2, 'message': message})

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class AddInvestmentProject(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
        result : add new investment to project investment table,
        requirements_1 : user must be logged in (LoginRequiredMixin),
        requirements_2: user mus have permission
          """
    permission_required = ('reports.add_investmentproject', 'reports.view_investmentproject', \
                           'reports.change_investmentproject', 'reports.delete_investmentproject')

    def get(self, request):
        """class  method,
            result : show add investment projects form,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('reports.add_investmentproject') and \
                request.user.has_perm('reports.view_investmentproject'):
            form = InvestmentForm
            return render(request, 'AddInvestmentProject.html', {'form': form, })

    def post(self, request):
        """class  method,
            result : show add investment project to investment project table,
            requirements: user must have permission"""

        if request.method == "POST" and 'add_project' in request.POST \
                and request.user.has_perm('reports.add_investmentproject') and \
                request.user.has_perm('reports.view_investmentproject'):
            form = InvestmentForm(request.POST)
            if form.is_valid():
                new_investment = InvestmentProject.objects.create(name=form.cleaned_data['name'],
                                                                  city=form.cleaned_data['city'],
                                                                  address=form.cleaned_data['address'],
                                                                  district=form.cleaned_data['district'],
                                                                  specification=form.cleaned_data['specification'],
                                                                  number_of_apartments=form.cleaned_data[
                                                                      'number_of_apartments'],
                                                                  start_date=form.cleaned_data['start_date'],
                                                                  finnish_date=form.cleaned_data['finnish_date'], )
                new_investment.save()
                message = f"Investment Project added successfully"
                return render(request, 'AddInvestmentProject.html', {'form': form, 'message': message, })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddInvestmentProject.html', {'form': form, 'message': message})

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class AddPricingPlan(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
           result : add new pricing plan to project investment table,
           requirements_1 : user must be logged in (LoginRequiredMixin),
           requirements_2: user mus have permission
             """
    permission_required = 'reports.add_pricingplan'

    def get(self, request):
        """class  method,
            result : show add pricing plan form to pricing plans,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('reports.add_pricingplan'):
            form_1 = PricingPlanForm_1
            form_2 = PricingPlanForm_2
            return render(request, 'AddPricingPlan.html', {'form_1': form_1,
                                                           'form_2': form_2, })

    def post(self, request):
        """class  method,
            result : add pricing plan to pricing plan table,
            requirements: user must have permission"""

        if request.method == "POST" and 'add_pricing_plan' in request.POST and \
                request.user.has_perm('reports.add_pricingplan'):
            form_1 = PricingPlanForm_1(request.POST)
            form_2 = PricingPlanForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                new_pricing_plan = PricingPlan.objects.create(
                    pricing_plan_name=form_1.cleaned_data['pricing_plan_name'],
                    pricing_plan_code=form_1.cleaned_data['pricing_plan_code'],
                    is_active=form_1.cleaned_data['is_active'],
                    nett_price=form_1.cleaned_data['nett_price'],
                    gross_price=form_1.cleaned_data['gross_price'],
                    nett_price_per_sqm=form_1.cleaned_data['nett_price_per_sqm'],
                    gross_price_per_sqm=form_1.cleaned_data['gross_price_per_sqm'], )
                new_pricing_plan.products.set(form_2.cleaned_data['products'])
                message = f"Pricing Plan added successfully"
                return render(request, 'AddPricingPlant.html', {'form_1': form_1, 'form_2': form_2, 'message': message,
                                                                })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddPricingPlan.html', {'form_1': form_1, 'form_2': form_2, 'message': message})

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
              result : show list of products per investment product table,
              requirements_1 : user must be logged in (LoginRequiredMixin),
              requirements_2: user mus have permission
                """
    permission_required = ('reports.add_product', 'reports.view_product', 'reports.delete_product', \
                           'reports.change_product',)

    def get(self, request):
        """class  method,
            result : show pick investment form ,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('reports.view_product') and \
                request.user.has_perm('reports.change_product'):
            product_by_investment_form = PickInvestment()
            return render(request, 'ShowProduct_pick_investment.html',
                          {'product_by_investment_form': product_by_investment_form, })

    def post(self, request):
        """class  method,
            result : show product list per investment project,
            requirements: user must have permission"""

        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST \
                and request.user.has_perm('reports.view_product') and request.user.has_perm('reports.change_product'):
            data = PickInvestment(request.POST)
            if data.is_valid():
                project_name = data.cleaned_data['investment']
                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).order_by('code')
                products = [val for val in product]
                return render(request, 'ShowProduct.html', {'products': products,
                                                            'project_name': project_name})
            else:
                message = f"Incorrect Product!"
                return render(request, 'ShowProduct.html', {'message': message})

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowProductData(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
                 result : show details of product, edit product, delete product
                 requirements_1 : user must be logged in (LoginRequiredMixin),
                 requirements_2: user mus have permission
                   """
    permission_required = ('reports.view_product', 'reports.change_product', 'reports.delete_product',
                           'reports.add_product')

    def get(self, request, *args, **kwargs):
        """class  method,
            result : show product data form,
            requirements: user must have permission"""

        if request.method == 'GET' and kwargs['product_id'] and request.user.has_perm('reports.view_product') and \
                request.user.has_perm('reports.change_product') and request.user.has_perm('reports.add_product'):
            product_id = kwargs['product_id']
            product = Product.objects.get(pk=product_id)
            form_product_basic_data = EditProductForm_1(initial=model_to_dict(product))
            form_product_rel_data = ProductForm_2(initial=model_to_dict(product))
            return render(request, 'ShowProductDetails.html', {'form_product_basic_data': form_product_basic_data,
                                                               'form_product_rel_data': form_product_rel_data, })
        # else:
        #     message = f"Product not found!"
        #     return render(request, 'ShowProductDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        """class  method,
            result : show product data, edit product, delete product,
            requirements: user must have permission"""

        if request.method == "POST" and EditProductForm_1(request.POST) and ProductForm_2(request.POST) \
                and 'save_product_data' in request.POST and request.user.has_perm('reports.view_product') and \
                request.user.has_perm('reports.add_product') and request.user.has_perm('reports.change_product'):

            product_id = kwargs['product_id']
            form_1 = EditProductForm_1(request.POST)
            form_2 = ProductForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                update_product = Product.objects.get(pk=form_1.cleaned_data['id'])
                form_1 = EditProductForm_1(request.POST, instance=update_product)
                form_2 = ProductForm_2(request.POST, instance=update_product)
                form_1.save()
                form_2.save()
                message = "Product data updated"
                return render(request, 'ShowProductDetails.html', {'message': message,
                                                                   'form_product_basic_data': form_1,
                                                                   'form_product_rel_data': form_2, })

            else:
                message = "Incorrect data!"
                product = Product.objects.get(pk=str(product_id))
                form_product_basic_data = EditProductForm_1(initial=model_to_dict(product))
                form_product_rel_data = ProductForm_2(initial=model_to_dict(product))
                return render(request, 'ShowProductDetails.html', {'message': message,
                                                                   'form_product_basic_data': form_product_basic_data,
                                                                   'form_product_rel_data': form_product_rel_data, })

        elif request.method == "POST" and EditProductForm_1(request.POST) and ProductForm_2(request.POST) \
                and 'delete_product' in request.POST and request.user.has_perm('reports.view_product') and \
                request.user.has_perm('reports.change_product')  \
                and request.user.has_perm('reports.view_product') and request.user.has_perm('reports.delete_product'):
            product_id = kwargs['product_id']
            product = Product.objects.get(pk=str(product_id))
            product.delete()
            message = "Product removed from data base!"
            return render(request, 'ShowProductDetails.html', {'message': message, })

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowInvestment(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
        result : show investment project list
        requirements_1 : user must be logged in (LoginRequiredMixin),
        requirements_2: user mus have permission"""

    permission_required = ('reports.view_investmentproject', 'reports.add_investmentproject', \
                           'reports.change_investmentproject', 'reports.delete_investmentproject')

    def get(self, request):
        """class method,
            result : show investment project list,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('reports.view_investmentproject') and \
                request.user.has_perm('reports.change_investmentproject'):
            investment_projects = InvestmentProject.objects.all()
            investment_projects_ls = [val for val in investment_projects]
            return render(request, 'PickInvestment.html',
                          {'investments': investment_projects_ls, })

    def post(self, request):
        """class method,
            result : show investment project details form, edit investment project, delete investment project,
            requirements: user must have permission"""

        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST \
                and request.user.has_perm('reports.view_investmentproject') and \
                request.user.has_perm('reports.change_investmentproject'):
            data = PickInvestment(request.POST)
            if data.is_valid():
                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).order_by('name')
                products = [val for val in product]
                return render(request, 'PickInvestment.html', {'products': products, })
            else:
                message = f"Incorrect Product!"
                return render(request, 'PickInvestment.html', {'message': message})

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowInvestmentData(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
        result : show investment project details, edit investment project, delete investment project
        requirements_1 : user must be logged in (LoginRequiredMixin),
        requirements_2: user mus have permission"""

    permission_required = ('reports.view_investmentproject', 'reports.add_investmentproject', \
                           'reports.change_investmentproject', 'reports.delete_investmentproject')

    def get(self, request, *args, **kwargs):
        """class method,
            result : show investment project details form, edit investment project, delete investment project,
            requirements: user must have permission"""

        if request.method == 'GET' and kwargs['investment_id'] and \
                request.user.has_perm('reports.view_investmentproject'):
            investment_id = kwargs['investment_id']
            investment = InvestmentProject.objects.get(pk=str(investment_id))
            form_investment_data = EditInvestmentForm(initial=model_to_dict(investment))
            return render(request, 'ShowInvestmentDetails.html', {'form_investment_data': form_investment_data, })
        else:
            message = f"Investment not found!"
            return render(request, 'ShowInvestmentDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        """class method,
            result : show investment project details edit investment project, delete investment project,
            requirements: user must have permission"""

        if request.method == "POST" and EditInvestmentForm(request.POST) and 'save_investment_data' \
                in request.POST and request.user.has_perm('reports.view_investmentproject') and \
                request.user.has_perm('reports.change_investmentproject') and \
                request.user.has_perm('reports.add_investmentproject'):
            investment_id = kwargs['investment_id']
            form = EditInvestmentForm(request.POST)
            if form.is_valid():
                update_investment = InvestmentProject.objects.get(pk=investment_id)
                form = EditInvestmentForm(request.POST, instance=update_investment)
                form.save()
                message = "Investment data updated"
                return render(request, 'ShowInvestmentDetails.html', {'message': message})
            else:
                message = "Incorrect data!"
                investment = InvestmentProject.objects.get(pk=str(investment_id))
                form_investment_data = EditInvestmentForm(initial=model_to_dict(investment))
                return render(request, 'ShowInvestmentDetails.html', {'form_investment_data': form_investment_data, })

        elif request.method == "POST" and EditInvestmentForm(request.POST) and 'delete_investment' in request.POST \
                and request.user.has_perm('reports.view_investmentproject') and \
                request.user.has_perm('reports.change_investmentproject') and \
                request.user.has_perm('reports.add_investmentproject') and \
                request.user.has_perm('reports.delete_investmentproject'):
            investment_id = kwargs['investment_id']
            investment = InvestmentProject.objects.get(pk=str(investment_id))
            investment.delete()
            message = "Investment removed from data base!"
            return render(request, 'ShowInvestmentDetails.html', {'message': message, })

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class AddUser(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
       result : add  user to users table,
       requirements_1 : user must be logged in (LoginRequiredMixin),
       requirements_2: user mus have permission"""

    permission_required = ('reports.add_user', 'reports.view_user')

    def get(self, request):
        """class  method ,
            result : show add user form,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('reports.add_user') \
                and request.user.has_perm('reports.view_user'):
            form_1 = UserForm
            form_2 = UserFormPassword
            return render(request, 'AddUser.html', {'form_1': form_1,
                                                    'form_2': form_2, })

    def post(self, request):
        """class  method ,
           result : add user to users table,
           requirements: user must have permission"""

        if request.method == "POST" and 'add_user' in request.POST and request.user.has_perm('reports.add_user') \
                and request.user.has_perm('reports.view_user'):
            form_1 = UserForm(request.POST)
            form_2 = UserFormPassword(request.POST)

            if form_1.is_valid() and form_2.is_valid():
                new_user = User.objects.create_user(username=form_1.cleaned_data['username'],
                                                    email=form_1.cleaned_data['email'], )

                new_user.set_password(form_2.cleaned_data['password'])
                new_user.save()
                message = f"User added successfully"
                return render(request, 'AddUser.html', {'form_1': form_1, 'form_2': form_2, 'message': message, })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddUser.html', {'form_1': form_1, 'form_2': form_2, 'message': message})

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowUser(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
               result : show user list,
               requirements_1 : user must be logged in (LoginRequiredMixin),
               requirements_2: user mus have permission"""

    permission_required = ('reports.add_user', 'reports.view_user')

    def get(self, request):
        """class  method ,
            result : show user list,
            requirements: user must have permission"""

        if request.method == 'GET' and request.user.has_perm('reports.add_user') \
                and request.user.has_perm('reports.view_user'):
            users = User.objects.all()
            users_projects_ls = [val for val in users]
            return render(request, 'ShowUsers.html',
                          {'users': users_projects_ls, })


class ShowUserData(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class based view,
                   result : show user details, edit user, delete user
                   requirements_1 : user must be logged in (LoginRequiredMixin),
                   requirements_2: user mus have permission"""

    permission_required = ('reports.add_user', 'reports.view_user', 'reports.delete_user')

    def get(self, request, *args, **kwargs):
        """class  method ,
           result : show user detail form ,
           requirements: user must have permission"""

        if request.method == 'GET' and kwargs['user_id'] and request.user.has_perm('reports.add_user') \
                and request.user.has_perm('reports.view_user'):
            user_id = kwargs['user_id']
            user = User.objects.get(pk=str(user_id))
            form_user_data_1 = UserForm(initial=model_to_dict(user))
            form_user_data_2 = UserFormPassword()
            return render(request, 'ShowUserDetails.html', {'form_user_details_data_1': form_user_data_1, \
                                                            'form_user_details_data_2': form_user_data_2, })
        else:
            message = f"User not found!"
            return render(request, 'ShowUserDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        """class  method,
           result : show user details, edit user , delete user
           requirements: user must have permission"""

        if request.method == "POST" and UserForm(request.POST) and UserFormPassword(request.POST) \
                and 'save_user_data' in request.POST and request.user.has_perm('reports.add_user') \
                and request.user.has_perm('reports.view_user') and request.user.has_perm('reports.change_user'):
            user_id = kwargs['user_id']
            form_1 = UserForm(request.POST)
            form_2 = UserFormPassword(request.POST)
            if form_1.is_valid():
                update_user = User.objects.get(pk=user_id)
                update_user.username = form_1.data['username']
                update_user.username = form_1.data['email']
                update_user.set_password(form_2.data['password'])
                update_user.save()
                message = "User data updated"
                return render(request, 'ShowUserDetails.html', {'message': message})
            else:
                message = "Incorrect data!"
                user = User.objects.get(pk=str(user_id))
                form_user_details_data_1 = UserForm(initial=model_to_dict(user))
                form_user_details_data_2 = UserFormPassword()
                return render(request, 'ShowUserDetails.html', {'message': message,
                                                                'form_user_details_data_1': form_user_details_data_1,
                                                                'form_user_details_data_2': form_user_details_data_2})

        elif request.method == "POST" and UserForm(request.POST) and 'delete_user' in request.POST and \
                request.user.has_perm('reports.add_user') and request.user.has_perm('reports.view_user') and \
                request.user.has_perm('reports.change_user') and request.user.has_perm('reports.delete_user'):
            user_id = kwargs['user_id']
            user = User.objects.get(pk=str(user_id))
            user.delete()
            message = "User removed from data base!"
            return render(request, 'ShowProductDetails.html', {'message': message, })

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowMenu(LoginRequiredMixin, View):
    """class based view,
              result : show menu based on permissions granted for user,
              requirements_1 : user must be logged in (LoginRequiredMixin),
              requirements_2: user mus have permission"""

    def get(self, request):
        """class  method,
           result : show user menu,
           requirements: user must have permission"""

        if request.method == "GET":
            user_type = request.user

            if user_type.is_superuser:

                ctx = {'menues': ["Client", "Product", 'Pricing Plan',
                                  'Investment Project', 'Salesperson', 'User', 'Reporting'],
                       'menu_client': {"Add Client": "http://127.0.0.1:8000/addClient/",
                                       "Show Client": "http://127.0.0.1:8000/showClient/"},
                       'menu_product': {"Add Product": "http://127.0.0.1:8000/addProduct/",
                                        "Show Product": "http://127.0.0.1:8000/showProduct/"},

                       'menu_pricing_plan': {"Add Pricing Plan": "http://127.0.0.1:8000/addPricingPlan/"},
                       'menu_investment': {"Show Investment Project": "http://127.0.0.1:8000/showInvestmentProject/",
                                           "Add Investment Project": "http://127.0.0.1:8000/addInvestmentProject/", },
                       'menu_salesperson': {"Show Salesperson": "http://127.0.0.1:8000/showSalesPerson/",
                                            "Add Salesperson": "http://127.0.0.1:8000/addSalesPerson/", },
                       'menu_user': {"Add User": "http://127.0.0.1:8000/addUser/",
                                     "Show User": "http://127.0.0.1:8000/showUser/", },
                       'menu_reporting': {"Search Product": "http://127.0.0.1:8000/productSearch/",
                                          "Search Product by Client": "http://127.0.0.1:8000/productByClient/",
                                          "Project Sales Analysis": "http://127.0.0.1:8000/salesAnalysis/",
                                          },


                       }


            else:
                ctx = {'menues': ["Client", "Product","Reporting"],
                       'menu_client': {"Add Client": "http://127.0.0.1:8000/addClient/",
                                       "Show Client": "http://127.0.0.1:8000/showClient/"},
                       'menu_product': {"Add Product": "http://127.0.0.1:8000/addProduct/",
                                        "Show Product": "http://127.0.0.1:8000/showProduct/"},

                       'menu_reporting': {"Search Product": "http://127.0.0.1:8000/productSearch/",
                                          "Search Product by Client": "http://127.0.0.1:8000/productByClient/",
                                          "Project Sales Analysis": "http://127.0.0.1:8000/salesAnalysis/", }
                       }

            return render(request, 'MainMenu.html', ctx)

    def post(self, request):
        """class  method,
           result : menu for user,
           requirements: user must have permission"""

        if request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class SearchApartment(LoginRequiredMixin, View):
    """class based view,
        result : list of products filtered by user,
        requirements_1 : user must be logged in (LoginRequiredMixin)"""

    def get(self, request):
        """class  method,
           result : show pick investment and filter form,
           requirements: user must be logged in (LoginRequiredMixin)"""

        if request.method == 'GET':
            product_by_investment_form = PickInvestment()
            filters = SalesFilterForm()
            ctx = {'product_by_investment_form': product_by_investment_form,
                          'sales_filter_form': filters,}
            return render(request, 'SearchProduct.html', ctx)


    def post(self, request):
        """class  method,
           result : show filtered data result,
           requirements: user must be logged in (LoginRequiredMixin)"""

        if request.method == "POST" and PickInvestment(request.POST) and SalesFilterForm(request.POST): #check method and forms
            data = PickInvestment(request.POST) #get data from form
            filter = SalesFilterForm(request.POST) #get data from form
            apartment_size = filter.data["area_range"] #get apartment size from filter form
            if apartment_size == '0-30': # check apartment area range
                range_min = 0
                range_max = 30
                size = (range_min, range_max)
            elif apartment_size == '30-40': # check apartment area range
                range_min = 30
                range_max = 40
                size = (range_min, range_max)
            elif apartment_size == '40-55': # check apartment area range
                range_min = 40
                range_max = 55
                size = (range_min, range_max)
            elif apartment_size == '55-75': # check apartment area range
                range_min = 55
                range_max = 75
                size = (range_min, range_max)
            elif apartment_size == '75-100': # check apartment area range
                range_min = 75
                range_max = 100
                size = (range_min, range_max)
            elif apartment_size == '100-140': # check apartment area range
                range_min = 100
                range_max = 140
                size = (range_min, range_max) # check apartment area range
            else:
                range_min = 0
                range_max = 500
                size = (range_min, range_max) # check apartment area range

            if data.is_valid() and filter.is_valid() and len(Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id),\
                    number_of_rooms=filter.data['number_of_rooms'] \
                    ,status=filter.data['status'],floor=filter.data['floor'],area__gt=size[0],area__lte=size[1]).order_by('code')) > 0: # filter validation
                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id),\
                    number_of_rooms=filter.data['number_of_rooms'] \
                    ,status=filter.data['status'],floor=filter.data['floor'],area__gt=size[0],area__lte=size[1]).order_by('code') # get list of products according to filters
                products = [val for val in product] # convert data into a list
                return render(request, 'SearchProduct.html', {'products': products, }) # push filtered product list to html template
            else:
                message = f"No products found!"
                return render(request, 'SearchProduct.html', {'message': message}) # push message if no products found

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')

class ProjectSalesAnalysis(LoginRequiredMixin, View):

    """class based view,
            result : set of sales statistics per project,
            requirements_1 : user must be logged in (LoginRequiredMixin)"""

    def get(self, request):
        """"class  method,
           result : show pick investment form
           requirements: user must be logged in (LoginRequiredMixin)"""

        if request.method == 'GET':
            product_by_investment_form = PickInvestment()
            # filters = SalesFilterForm()
            ctx = {'product_by_investment_form': product_by_investment_form,}
            return render(request, 'ProjectSalesAnalysis.html', ctx)


    def post(self, request):
        """"class  method,
           result : show sales results per investment
           requirements: user must be logged in (LoginRequiredMixin)"""

        if request.method == "POST" and PickInvestment(request.POST):  # check request method and if form in request
            data = PickInvestment(request.POST)  # get data frm form

            if data.is_valid() and len(Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).order_by('code')) > 0: # check if form is valid

                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).order_by('code') # get product data

                products = [val for val in product] # convert product data to a list

                products_sold = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).filter(status="sold").order_by('code')

                products_reserved = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).filter(
                    status="reserved").order_by('code')

                products_available = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id)).filter(
                    status="available").order_by('code')
                project_name = data.cleaned_data['investment']


                sold_products_qty = len(Product.objects.all().filter(
                    investments= InvestmentProject.objects.get(id=data.cleaned_data['investment'].id),status='sold')) # get sold products qty
                reserved_products_qty = len(Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id), status='reserved')) # get  reserved products qty
                available_products_qty = len(Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id), status='available')) # get available products qty
                sold_products_area = Product.objects.all().filter(
                    investments= InvestmentProject.objects.get(id=data.cleaned_data['investment'].id),status='sold').values_list("area") # get sold products area data
                reserved_products_area = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id), status='reserved').values_list("area") # get reserved products area data
                available_products_area = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id), status='available').values_list("area") # get available products area data

                sold_products_value = Product.objects.all().filter(
                    investments= InvestmentProject.objects.get(id=data.cleaned_data['investment'].id),status='sold').values_list("price") # get  sold products sales value data
                reserved_products_value = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id), status='reserved').values_list("price") # get  reserved products sales value data
                available_products_value = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id), status='available').values_list("price") # get  available products sales value data

                total_apartments_qty = sold_products_qty + reserved_products_qty + available_products_qty # calculate total apartments quantity
                sold_products_share = f"{round(float(sold_products_qty/total_apartments_qty*100),2)} %" # calculate sold apartments qty share
                reserved_products_share = f"{round(float(reserved_products_qty/total_apartments_qty*100),2)} %" # calculate reseved apartments qty share
                available_products_share = f"{round(float(available_products_qty/total_apartments_qty*100),2)} %" # calculate available apartments qty share


                sold_products_area_val = sum([val[0] for val in sold_products_area]) # calculate sold apartments area
                reserved_products_area_val = sum([val[0] for val in reserved_products_area]) # calculate reserved apartments area
                available_products_area_val = sum([val[0] for val in available_products_area]) # calculate available apartments area
                total_apartments_area_val = sold_products_area_val + reserved_products_area_val + available_products_area_val # calculate total apartments area

                sold_products_area_share = f"{round(float(sold_products_area_val / total_apartments_area_val * 100), 2)} %" # calculate sold apartments area share
                reserved_products_area_share = f"{round(float(reserved_products_area_val / total_apartments_area_val * 100), 2)} %" # calculate reserved apartments area share
                available_products_area_share = f"{round(float(available_products_area_val / total_apartments_area_val * 100), 2)} %" # calculate available apartments area share

                sold_products_val = sum([val[0] for val in sold_products_value])  # calculate sold apartments value
                reserved_products_val = sum([val[0] for val in reserved_products_value])  # calculate reserved apartments value
                available_products_val = sum([val[0] for val in available_products_value])  # calculate available apartments value
                total_apartments_val = sold_products_val + reserved_products_val + available_products_val  # calculate total apartments value

                if sold_products_area_val == 0:
                    average_sold_price_per_sqm = 0
                else:
                    average_sold_price_per_sqm = f"{round(float(sold_products_val / sold_products_area_val), 2)} PLN" # calculate sold apartments average price/sqm

                if reserved_products_area_val == 0:
                    average_reserved_price_per_sqm = 0
                else:
                    average_reserved_price_per_sqm = f"{round(float(reserved_products_val / reserved_products_area_val), 2)} PLN" # calculate reserved apartments average price/sqm

                if available_products_area_val == 0:

                    average_available_price_per_sqm = 0
                else:
                    average_available_price_per_sqm = f"{round(float(available_products_val / available_products_area_val), 2)} PLN" # calculate available apartments average price/sqm

                if total_apartments_area_val == 0:
                    average_total_price_per_sqm = 0
                else:
                    average_total_price_per_sqm = f"{round(float(total_apartments_val / total_apartments_area_val), 2)} PLN" # calculate total average

                if sold_products_area_val == 0:
                    average_sold_price = 0
                else:
                    average_sold_price = int(sold_products_val / sold_products_area_val)  # calculate sold apartments average price/sqm

                if reserved_products_area_val == 0:
                    average_reserved_price = 0
                else:
                    average_reserved_price = int(reserved_products_val / reserved_products_area_val) # calculate reserved apartments average price/sqm

                if available_products_area_val == 0:
                    average_available_price = 0
                else:
                    average_available_price = int(
                        available_products_val / available_products_area_val)  # calculate available apartments average price/sqm

                if total_apartments_area_val == 0:
                    average_total_price = 0
                else:

                    average_total_price = int(total_apartments_val / total_apartments_area_val) # calculate total average price/sqm


                # labels = 'Sold', 'Reserved', 'Available'
                # areas = [sold_products_area_val, reserved_products_area_val, available_products_area_val]
                # explode = (0.1, 0, 0)
                # ax1 = matplotlib.pyplot.subplot()
                # ax1.pie(areas, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                # ax1.axis('equal')
                # matplotlib.pyplot.savefig('/home/karol/Coderslab_final_project/simple_crm/cstmgmnt/static/pie_chart.png')
                # p_chart_1 = Image.open('/home/karol/Coderslab_final_project/simple_crm/cstmgmnt/static/pie_chart.png')

                # columns = ['Sold', 'Reserved', 'Available', 'Total']
                # prices = [average_sold_price, average_reserved_price, average_available_price, average_total_price]
                # matplotlib.pyplot.bar(range(len(columns)), prices)
                # matplotlib.pyplot.ylabel("Price per sqm")
                # matplotlib.pyplot.title("Average prices")
                # matplotlib.pyplot.xticks(range(len(columns)), columns)
                # matplotlib.pyplot.savefig('/home/karol/Coderslab_final_project/simple_crm/cstmgmnt/static/bar_chart.png')





                ctx = {'project': project_name,
                       # 'pie_chart': p_chart_1,
                       'average_sold_price':average_sold_price,
                       'average_reserved_price':average_reserved_price,
                       'average_available_price':average_available_price,
                       'average_total_price':average_total_price,
                           'products_sold': products_sold,
                       'products_reserved': products_reserved,
                       'products_available': products_available,
                       'total_apartments_quantity': total_apartments_qty,
                       'sold_apartments_quantity': sold_products_qty,
                       'reserved_apartments_quantity': reserved_products_qty,
                       'available_apartments_quantity': available_products_qty,
                       'sold_products_share' : sold_products_share,
                       'reserved_products_share' : reserved_products_share,
                        'available_products_share': available_products_share,
                       'total_apartments_area' :f"{total_apartments_area_val} sqm",
                       'sold_apartments_area' : f"{sold_products_area_val} sqm",
                        'reserved_apartments_area': f"{reserved_products_area_val} sqm",
                       'available_apartments_area': f"{available_products_area_val} sqm",
                        'sold_apartments_area_share' : sold_products_area_share,
                        'reserved_apartments_area_share': reserved_products_area_share,
                       'available_apartments_area_share': available_products_area_share,
                        'total_apartments_val': total_apartments_val,
                        'sold_products_val': sold_products_val,
                        'reserved_products_val': reserved_products_val,
                        'available_products_val': available_products_val,
                        'average_total_price_per_sqm': average_total_price_per_sqm,
                        'average_sold_price_per_sqm' : average_sold_price_per_sqm,
                        'average_reserved_price_per_sqm' : average_reserved_price_per_sqm,
                        'average_available_price_per_sqm' : average_available_price_per_sqm,} # pass data to contex
                return render(request, 'SalesAnalysisPerProject.html', ctx) # pass data to html
            else:
                message = f"No products found!"
                return render(request, 'SalesAnalysisPerProject.html', {'message': message}) # pass message to html if products not found

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')


class ShowProductByClient(LoginRequiredMixin, View):
    """class based view,
        result : list of products filtered by client,
        requirements_1 : user must be logged in (LoginRequiredMixin)"""

    def get(self, request):
        """class  method,
           result : show pick client and filter form,
           requirements: user must be logged in (LoginRequiredMixin)"""

        if request.method == 'GET':
            product_by_client_form = PickClient()
            ctx = {'product_by_client_form': product_by_client_form,}
            return render(request, 'ShowProduct_pick_client.html', ctx)


    def post(self, request):
        """class  method,
           result : show products of client,
           requirements: user must be logged in (LoginRequiredMixin)"""

        if request.method == "POST" and PickClient(request.POST): #check method and forms
            client_data = PickClient(request.POST)
            client = Client.objects.get(pk=client_data.data['name']) #get client from form
            if client_data.is_valid() and len(client.products.all()) > 0 : # filter validation
                product = client.products.all()  # get list of products according to filters
                products = [val for val in product] # convert data into a list
                return render(request, 'ShowProductbyClient.html', {'products': products, }) # push filtered product list to html
            else:
                message = f"No products found!"
                return render(request, 'ShowProductbyClient.html.html', {'message': message}) # push message if no products found

        elif request.method == "POST" and 'logout' in request.POST:
            logout(request)
            return redirect('/loginPage/')
