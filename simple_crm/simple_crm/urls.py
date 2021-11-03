"""simple_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from cstmgmnt.views import AddClient,AddSalesPerson,ShowClientData,ShowClient,ShowSalesPerson, ShowSalesPersonData, ValidateUser
from reports.views import AddProduct, AddInvestmentProject, AddPricingPlan, ShowProduct, ShowProductData, ShowInvestment, ShowInvestmentData,AddUser,ShowUser,ShowUserData

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', AddClient.as_view()),
    path('addSalesPerson/', AddSalesPerson.as_view()),
    path('showSalesPerson/', ShowSalesPerson.as_view()),
    path('showSalesPerson/<str:salesperson_id>/', ShowSalesPersonData.as_view()),
    path('addClient/', AddClient.as_view()),
    path('showClient/<str:client_id>/', ShowClientData.as_view()),
    path('showClient/', ShowClient.as_view()),
    path('addProduct/', AddProduct.as_view()),
    path('addInvestmentProject/', AddInvestmentProject.as_view()),
    path('addPricingPlan/', AddPricingPlan.as_view()),
    path('showProduct/', ShowProduct.as_view()),
    path('showProduct/<str:product_id>', ShowProductData.as_view()),
    path('showInvestmentProject/', ShowInvestment.as_view()),
    path('showInvestmentProject/<str:investment_id>', ShowInvestmentData.as_view()),
    path('addUser/', AddUser.as_view()),
    path('showUser/', ShowUser.as_view()),
    path('editUser/<str:user_id>', ShowUserData.as_view()),
    path('loginPage/', ValidateUser.as_view()),




]
