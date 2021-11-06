from django.shortcuts import render
from reports.forms import ProductForm_1, ProductForm_2, InvestmentForm, PricingPlanForm_1 , PricingPlanForm_2, EditProductForm_1, EditInvestmentForm, UserForm,UserFormPassword
from django.views import View
from reports.models import Product, PricingPlan, InvestmentProject
from cstmgmnt.forms import PickInvestment
from django.forms import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

class AddProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('reports.add_product', 'reports.show_product')
    def get(self, request):
        if request.method == 'GET' and request.user.has_perm(permission_required):
            form_1 = ProductForm_1
            form_2 = ProductForm_2

            return render(request, 'AddProduct.html', {'form_1': form_1,
                                                      'form_2': form_2, })

    def post(self, request):
        if request.method == "POST" and request.user.has_perm(permission_required):
            form_1 = ProductForm_1(request.POST)
            form_2 = ProductForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                new_product = Product.objects.create(code=form_1.cleaned_data['code'],
                                                   direction=form_1.cleaned_data['direction'],
                                                   floor=form_1.cleaned_data['floor'],
                                                   number_of_rooms=form_1.cleaned_data['number_of_rooms'],
                                                   rating=form_1.cleaned_data['rating'],
                                                   balcony=form_1.cleaned_data['balcony'],
                                                   loggia=form_1.cleaned_data['loggia'],
                                                   status=form_1.cleaned_data['status'],
                                                   price=form_1.cleaned_data['price'])

                new_product.investments.set(form_2.cleaned_data['investments'])

                message = f"Product added successfully"
                return render(request, 'AddProduct.html', {'form_1': form_1, 'form_2': form_2, 'message': message, })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddProduct.html', {'form_1': form_1, 'form_2': form_2, 'message': message})


class AddInvestmentProject(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.add_investmentproject','reports.show_investmentproject')
    def get(self, request):
        if request.method == 'GET' and request.user.has_perm(permission_required):
            form = InvestmentForm
            return render(request, 'AddInvestmentProject.html', {'form': form,})

    def post(self, request):
        if request.method == "POST" and request.user.has_perm(permission_required):
            form = InvestmentForm(request.POST)
            if form.is_valid():
                new_investment = InvestmentProject.objects.create(name=form.cleaned_data['name'],
                                                   city=form.cleaned_data['city'],
                                                   address=form.cleaned_data['address'],
                                                   district=form.cleaned_data['district'],
                                                   specification=form.cleaned_data['specification'],
                                                   number_of_apartments=form.cleaned_data['number_of_apartments'],
                                                   start_date=form.cleaned_data['start_date'],
                                                   finnish_date=form.cleaned_data['finnish_date'],)

                message = f"Investment Project added successfully"
                return render(request, 'AddInvestmentProject.html', {'form': form, 'message': message, })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddInvestmentProject.html', {'form': form, 'message': message})

class AddPricingPlan(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = 'reports.add_pricingplan'
    def get(self, request):
        if request.method == 'GET' and request.user.has_perm(permission_required):
            form_1 = PricingPlanForm_1
            form_2 = PricingPlanForm_2
            return render(request, 'AddPricingPlan.html', {'form_1': form_1,
                                                      'form_2': form_2,})

    def post(self, request):
        if request.method == "POST" and request.user.has_perm(permission_required):
            form_1 = PricingPlanForm_1(request.POST)
            form_2 = PricingPlanForm_2(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                new_pricing_plan = PricingPlan.objects.create(pricing_plan_name=form_1.cleaned_data['pricing_plan_name'],
                                                   pricing_plan_code=form_1.cleaned_data['pricing_plan_code'],
                                                   is_active=form_1.cleaned_data['is_active'],
                                                   nett_price=form_1.cleaned_data['nett_price'],
                                                   gross_price=form_1.cleaned_data['gross_price'],
                                                   nett_price_per_sqm=form_1.cleaned_data['nett_price_per_sqm'],
                                                   gross_price_per_sqm=form_1.cleaned_data['gross_price_per_sqm'],)
                new_pricing_plan.products.set(form_2.cleaned_data['products'])
                message = f"Pricing Plan added successfully"
                return render(request, 'AddPricingPlant.html', {'form_1': form_1, 'form_2': form_2, 'message': message, })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddPricingPlan.html', {'form_1': form_1, 'form_2': form_2, 'message': message})


class ShowProduct(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.show_product')
    def get(self, request):
        if request.method == 'GET' and request.user.has_perm(permission_required):
            product_by_investment_form = PickInvestment()
            return render(request, 'ShowProduct_pick_investment.html',
                          {'product_by_investment_form': product_by_investment_form, })

    def post(self, request):
        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST and request.user.has_perm(permission_required):
            data = PickInvestment(request.POST)
            if data.is_valid():
                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id))
                products = [val for val in product]
                return render(request, 'ShowProduct.html', {'products': products,})
            else:
                message = f"Incorrect Product!"
                return render(request, 'ShowProduct.html', {'message': message})


class ShowProductData(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.show_product','reports.change_product','reports.delete_product')
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and kwargs['product_id'] and request.user.has_perm(permission_required):
            product_id = kwargs['product_id']
            product = Product.objects.get(pk=str(product_id))
            form_product_basic_data = EditProductForm_1(initial=model_to_dict(product))
            form_product_rel_data = ProductForm_2(initial=model_to_dict(product))
            return render(request, 'ShowProductDetails.html', {'form_product_basic_data': form_product_basic_data,
                                                              'form_product_rel_data': form_product_rel_data, })
        else:
            message = f"Client not found!"
            return render(request, 'ShowProductDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and EditProductForm_1(request.POST) and ProductForm_2(request.POST) \
                and 'save_product_data' and request.user.has_perm(permission_required) in request.POST:
            product_id = kwargs['product_id']
            form_1 = EditProductForm_1(request.POST)
            form_2 = EditProductForm_1(request.POST)
            if form_1.is_valid() and form_2.is_valid():
                update_client = Product.objects.get(pk=form_1.cleaned_data['id'])
                form_1 = EditProductForm_1(request.POST, instance=update_client)
                form_2 = ProductForm_2(request.POST, instance=update_client)
                form_1.save()
                form_2.save()
                message = "Product data updated"
                return render(request, 'ShowProductDetails.html', {'message': message})
            else:
                message = "Incorrect data!"
                product = Product.objects.get(pk=str(product_id))
                form_client_basic_data = EditProductForm_1(initial=model_to_dict(product))
                form_client_rel_data = ProductForm_2(initial=model_to_dict(product))
                return render(request, 'ShowClientDetails.html', {'message': message,
                                                                  'form_client_basic_data': form_client_basic_data,
                                                                  'form_client_rel_data': form_client_rel_data, })

        if request.method == "POST" and EditProductForm_1(request.POST) and ProductForm_2(request.POST) \
                and 'delete_product' and request.user.has_perm(permission_required) in request.POST:
            product_id = kwargs['product_id']
            product = Product.objects.get(pk=str(product_id))
            product.delete()
            message = "Product removed from data base!"
            return render(request, 'ShowProductDetails.html', {'message': message, })

class ShowInvestment(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.show_investmentproject')
    def get(self, request):
        if request.method == 'GET' and request.user.has_perm(permission_required):
            investment_projects = InvestmentProject.objects.all()
            investment_projects_ls = [val for val in investment_projects]
            return render(request, 'PickInvestment.html',
                          {'investments': investment_projects_ls, })

    def post(self, request):
        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST and request.user.has_perm(permission_required):
            data = PickInvestment(request.POST)
            if data.is_valid():
                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id))
                products = [val for val in product]
                return render(request, 'PickInvestment.html', {'products': products,})
            else:
                message = f"Incorrect Product!"
                return render(request, 'PickInvestment.html', {'message': message})

class ShowInvestmentData(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.show_investmentproject', 'reports.change_investmentproject', 'reports.delete_investmentproject')
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and kwargs['investment_id'] and request.user.has_perm(permission_required):
            investment_id = kwargs['investment_id']
            investment = InvestmentProject.objects.get(pk=str(investment_id))
            form_investment_data = EditInvestmentForm(initial=model_to_dict(investment))
            return render(request, 'ShowInvestmentDetails.html', {'form_investment_data': form_investment_data, })
        else:
            message = f"Investment not found!"
            return render(request, 'ShowInvestmentDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and EditInvestmentForm(request.POST) and 'save_investment_data' and request.user.has_perm(permission_required) in request.POST:
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

        if request.method == "POST" and EditInvestmentForm(request.POST) and 'delete_investment' and request.user.has_perm(permission_required) in request.POST:
            investment_id = kwargs['investment_id']
            investment = InvestmentProject.objects.get(pk=str(investment_id))
            investment.delete()
            message = "Investment removed from data base!"
            return render(request, 'ShowInvestmentDetails.html', {'message': message, })


class AddUser(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.add_user','reports.show_user')
    def get(self, request):
        if request.method == 'GET' and request.user.has_perm(permission_required):
            form_1 = UserForm
            form_2 = UserFormPassword
            return render(request, 'AddUser.html', {'form_1': form_1,
                                                    'form_2': form_2, })

    def post(self, request):
        if request.method == "POST" and request.user.has_perm(permission_required):
            form_1 = UserForm(request.POST)
            form_2 = UserFormPassword(request.POST)

            if form_1.is_valid() and form_2.is_valid():
                new_user = User.objects.create_user(username=form_1.cleaned_data['username'],
                                                                  email=form_1.cleaned_data['email'],)

                new_user.set_password(form_2.cleaned_data['password'])
                new_user.save()
                message = f"User added successfully"
                return render(request, 'AddUser.html', {'form_1': form_1,'form_2': form_2, 'message': message, })
            else:
                message = f"Incorrect data!"
                return render(request, 'AddUser.html', {'form_1': form_1,'form_2': form_2, 'message': message})

class ShowUser(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.add_user', 'reports.show_user','reports.delete_user')
    def get(self, request):
        if request.method == 'GET' and request.user.has_perm(permission_required):
            users = User.objects.all()
            users_projects_ls = [val for val in users]
            return render(request, 'ShowUsers.html',
                          {'users': users_projects_ls, })


class ShowUserData(LoginRequiredMixin, PermissionRequiredMixin,View):
    permission_required = ('reports.add_user', 'reports.show_user', 'reports.delete_user')
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and kwargs['user_id'] and request.user.has_perm(permission_required):
            user_id = kwargs['user_id']
            user = User.objects.get(pk=str(user_id))
            form_user_data_1 = UserForm(initial=model_to_dict(user))
            form_user_data_2 = UserFormPassword()
            return render(request, 'ShowUserDetails.html', {'form_user_details_data_1': form_user_data_1, 'form_user_details_data_2': form_user_data_2, })
        else:
            message = f"User not found!"
            return render(request, 'ShowUserDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and UserForm(request.POST) and UserFormPassword(request.POST)  \
                and 'save_user_data' and request.user.has_perm(permission_required) in request.POST:
            user_id = kwargs['user_id']
            form_1 = UserForm(request.POST)
            form_2 = UserFormPassword(request.POST)
            if form_1.is_valid():
                update_user = User.objects.get(pk=user_id)
                form_1 = UserForm(request.POST, instance=update_user)
                form_2 = UserFormPassword(request.POST)
                password = form_2.cleaned_data['password']
                update_user.set_password(password)
                update_user.save()
                form_1.save()
                message = "User data updated"
                return render(request, 'ShowUserDetails.html', {'message': message})
            else:
                message = "Incorrect data!"
                user = User.objects.get(pk=str(user_id))
                form_user_details_data_1 = UserForm(initial=model_to_dict(user))
                form_user_details_data_2 = UserFormPassword()
                return render(request, 'ShowUserDetails.html', {'message': message,
                                                                  'form_user_details_data_1': form_user_details_data_1,
                                                                'form_user_details_data_2': form_user_details_data_2 })

        if request.method == "POST" and UserForm(request.POST)   and 'delete_user' and request.user.has_perm(permission_required) in request.POST:
            user_id = kwargs['user_id']
            user = User.objects.get(pk=str(user_id))
            user.delete()
            message = "User removed from data base!"
            return render(request, 'ShowProductDetails.html', {'message': message, })

class ShowMenu(LoginRequiredMixin, PermissionRequiredMixin,View):
    def get(self, request):
        if request.method == "GET":
            user_type = request.user
            if user_type.is_superuser:

                ctx = {'menues': ["Client","Product",'Pricing Plan',
                                   'Investment Project','Salesperson','User'],
                        'menu_client': {"Add Client": "http://127.0.0.1:8000/addClient/",
                                        "Show Client": "http://127.0.0.1:8000/showClient/"},
                        'menu_product': {"Add Product": "http://127.0.0.1:8000/addProduct/",
                                        "Show Product": "http://127.0.0.1:8000/showProduct/"},
                        'menu_pricing_plan': {"Add Pricing Plan": "http://127.0.0.1:8000/addPricingPlan/"},
                        'menu_investment': {"Show Investment Project": "http://127.0.0.1:8000/showInvestmentProject/",
                                        "Add Investment Project": "http://127.0.0.1:8000/addInvestmentProject/",},
                        'menu_salesperson': {"Show Salesperson": "http://127.0.0.1:8000/showSalesPerson/",
                                            "Add Salesperson": "http://127.0.0.1:8000/addSalesPerson/",},
                        'menu_user': {"Add User": "http://127.0.0.1:8000/addUser/",
                                    "Show User": "http://127.0.0.1:8000/showUser/",}}





            else:
                ctx = {'menues': ["Client","Product"],
                        'menu_client': {"Add Client": "http://127.0.0.1:8000/addClient/",
                                        "Show Client": "http://127.0.0.1:8000/showClient/"},
                         'menu_product':{"Add Product": "http://127.0.0.1:8000/addProduct/",
                                        "Show Product": "http://127.0.0.1:8000/showProduct/"},}



            return render(request, 'MainMenu.html', ctx)
