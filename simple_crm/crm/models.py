
from django.utils import timezone


from django.db import models

from rep.models import Product, InvestmentProject, PricingPlan

contact_type = [
    ('email', 'email'),
    ('phone', 'phone'),
    ]


class Client(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    post_code = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    preferred_contact_type = models.CharField(max_length=255, choices=contact_type, null=True)
    additional_info = models.TextField(null=True)
    investments = models.ManyToManyField(InvestmentProject)
    products = models.ManyToManyField(Product, through='ClientProductThrough')

class ClientProductThrough(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_of_link = models.DateTimeField(default=timezone.now(),null=False)



class SalesPerson(models.Model):
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    login = models.CharField(max_length=64, null=False)
    password = models.CharField(max_length=128, null=True)
    investments = models.ManyToManyField(InvestmentProject)
    products = models.ManyToManyField(Product, through='SalesPersonProduct')
    clients = models.ManyToManyField(Client)


class SalesPersonProduct(models.Model):
    salesperson = models.ForeignKey(SalesPerson, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_of_link = models.DateTimeField(default=timezone.now(), null=False)









