from django.db import models

available_floor = [
    ('1', '1st',),
    ('2', '2nd'),
    ('3', '3rd'),
    ('4', '4th'),
    ('5', '5th'),
    ('6', '6th'),
    ('7', '7th'),
    ('8', '8th'),
    ('9', '9th'),
    ('10', '10th'),
    ('11', '11th'),
    ('12', '12th'),
    ('13', '13th'),
    ('14', '14th'),
    ('15', '15th'),
]
available_rooms = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
]

overall_apartment_score = [
    ('60%', '60%'),
    ('70%', '70%'),
    ('80%', '80%'),
    ('90%', '90%'),
]

direction = [
    ('north', 'north'),
    ('south', 'south'),
    ('east', 'east'),
    ('west', 'west'),
    ('north-east', 'north-east'),
    ('north-west', 'north-west'),
    ('south-east', 'south-east'),
    ('south-west', 'south-west'),
    ('east-west', 'east-west'),
    ('north-south', 'north-south'),
]

product_status = [
    ('available', 'available'),
    ('reserved', 'reserved'),
    ('sold', 'sold'),
]

district = [
    ('center area', 'center area'),
    ('sub urban', 'sub urban'),
    ('business district', 'business district'),
    ('midtown', 'midtown'),
    ('outer center area', 'outer center area'),
]


class InvestmentProject(models.Model):
    name = models.CharField(max_length=128, null=False)
    city = models.CharField(max_length=128, null=False)
    address = models.CharField(max_length=255, null=False)
    district = models.CharField(max_length=128, choices=district, null=False)
    specification = models.TextField(null=True)
    number_of_apartments = models.IntegerField(null=True)
    start_date = models.DateField(null=False)
    finnish_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.name} "


class Product(models.Model):
    code = models.CharField(max_length=128, null=False)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    direction = models.CharField(max_length=128, choices=direction, null=False)
    floor = models.CharField(max_length=128, choices=available_floor, null=False)
    number_of_rooms = models.CharField(max_length=128, choices=available_rooms, null=False)
    rating = models.CharField(max_length=128, choices=overall_apartment_score, null=False)
    balcony = models.BooleanField(default=False)
    loggia = models.BooleanField(default=False)
    status = models.CharField(max_length=128, choices=product_status, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    investments = models.ForeignKey(InvestmentProject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code}"


class PricingPlan(models.Model):
    pricing_plan_name = models.CharField(max_length=128)
    pricing_plan_code = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    nett_price = models.DecimalField(max_digits=128, decimal_places=2)
    gross_price = models.DecimalField(max_digits=128, decimal_places=2)
    nett_price_per_sqm = models.DecimalField(max_digits=128, decimal_places=2)
    gross_price_per_sqm = models.DecimalField(max_digits=128, decimal_places=2)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.pricing_plan_code}"
