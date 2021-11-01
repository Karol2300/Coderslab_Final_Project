from django.shortcuts import render
from reports.forms import ProductForm_1, ProductForm_2, InvestmentForm, PricingPlanForm_1 , PricingPlanForm_2, EditProductForm_1, EditInvestmentForm
from django.views import View
from reports.models import Product, PricingPlan, InvestmentProject
from cstmgmnt.forms import PickInvestment
from django.forms import model_to_dict

class AddProduct(View):
    def get(self, request):
        if request.method == 'GET':
            form_1 = ProductForm_1
            form_2 = ProductForm_2

            return render(request, 'AddProduct.html', {'form_1': form_1,
                                                      'form_2': form_2, })

    def post(self, request):
        if request.method == "POST":
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


class AddInvestmentProject(View):
    def get(self, request):
        if request.method == 'GET':
            form = InvestmentForm
            return render(request, 'AddInvestmentProject.html', {'form': form,})

    def post(self, request):
        if request.method == "POST":
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

class AddPricingPlan(View):
    def get(self, request):
        if request.method == 'GET':
            form_1 = PricingPlanForm_1
            form_2 = PricingPlanForm_2
            return render(request, 'AddPricingPlan.html', {'form_1': form_1,
                                                      'form_2': form_2,})

    def post(self, request):
        if request.method == "POST":
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


class ShowProduct(View):
    def get(self, request):
        if request.method == 'GET':
            product_by_investment_form = PickInvestment()
            return render(request, 'ShowProduct_pick_investment.html',
                          {'product_by_investment_form': product_by_investment_form, })

    def post(self, request):
        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST:
            data = PickInvestment(request.POST)
            if data.is_valid():
                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id))
                products = [val for val in product]
                return render(request, 'ShowProduct.html', {'products': products,})
            else:
                message = f"Incorrect Product!"
                return render(request, 'ShowProduct.html', {'message': message})


class ShowProductData(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and kwargs['product_id']:
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
                and 'save_product_data' in request.POST:
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
                and 'delete_product' in request.POST:
            product_id = kwargs['product_id']
            product = Product.objects.get(pk=str(product_id))
            product.delete()
            message = "Product removed from data base!"
            return render(request, 'ShowProductDetails.html', {'message': message, })

class ShowInvestment(View):
    def get(self, request):
        if request.method == 'GET':
            investment_projects = InvestmentProject.objects.all()
            investment_projects_ls = [val for val in investment_projects]
            return render(request, 'PickInvestment.html',
                          {'investments': investment_projects_ls, })

    def post(self, request):
        if request.method == "POST" and PickInvestment(request.POST) and 'investment_form' in request.POST:
            data = PickInvestment(request.POST)
            if data.is_valid():
                product = Product.objects.all().filter(
                    investments=InvestmentProject.objects.get(id=data.cleaned_data['investment'].id))
                products = [val for val in product]
                return render(request, 'PickInvestment.html', {'products': products,})
            else:
                message = f"Incorrect Product!"
                return render(request, 'PickInvestment.html', {'message': message})

class ShowInvestmentData(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and kwargs['investment_id']:
            investment_id = kwargs['investment_id']
            investment = InvestmentProject.objects.get(pk=str(investment_id))
            form_investment_data = EditInvestmentForm(initial=model_to_dict(investment))
            return render(request, 'ShowInvestmentDetails.html', {'form_investment_data': form_investment_data, })
        else:
            message = f"Investment not found!"
            return render(request, 'ShowInvestmentDetails.html', {'message': message, })

    def post(self, request, *args, **kwargs):
        if request.method == "POST" and EditInvestmentForm(request.POST) and 'save_investment_data' in request.POST:
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

        if request.method == "POST" and EditInvestmentForm(request.POST) and 'delete_investment' in request.POST:
            investment_id = kwargs['investment_id']
            investment = InvestmentProject.objects.get(pk=str(investment_id))
            investment.delete()
            message = "Investment removed from data base!"
            return render(request, 'ShowInvestmentDetails.html', {'message': message, })
