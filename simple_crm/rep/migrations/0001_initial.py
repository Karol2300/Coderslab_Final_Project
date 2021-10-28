# Generated by Django 3.2.8 on 2021-10-24 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, null=None)),
                ('city', models.CharField(max_length=64, null=None)),
                ('address', models.TextField(null=None)),
                ('district', models.CharField(choices=[('center area', 'center area'), ('sub urban', 'sub urban'), ('business district', 'business district'), ('midtown', 'midtown'), ('outer center area', 'outer center area')], max_length=64, null=None)),
                ('specification', models.TextField()),
                ('start_date', models.DateTimeField(null=None)),
                ('finnish_date', models.DateTimeField(null=None)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=64)),
                ('area', models.DecimalField(decimal_places=2, max_digits=20)),
                ('direction', models.CharField(choices=[('north', 'north'), ('south', 'south'), ('east', 'east'), ('west', 'west'), ('north-east', 'north-east'), ('north-west', 'north-west'), ('south-east', 'south-east'), ('south-west', 'south-west'), ('east-west', 'east-west')], max_length=64)),
                ('floor', models.CharField(choices=[('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th'), ('5', '5th'), ('6', '6th'), ('7', '7th'), ('8', '8th'), ('9', '9th'), ('10', '10th'), ('11', '11th'), ('12', '12th'), ('13', '13th'), ('14', '14th'), ('15', '15th')], max_length=64)),
                ('number_of_rooms', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=64)),
                ('rating', models.CharField(choices=[('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%')], max_length=64)),
                ('balcony', models.BooleanField()),
                ('loggia', models.BooleanField()),
                ('status', models.CharField(choices=[('available', 'available'), ('reserved', 'reserved'), ('sold', 'sold')], max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('investments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rep.investmentproject')),
            ],
        ),
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pricing_name', models.CharField(max_length=64)),
                ('is_active', models.BooleanField()),
                ('nett_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('gross_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('nett_price_per_sqm', models.DecimalField(decimal_places=2, max_digits=20)),
                ('gross_price_per_sqm', models.DecimalField(decimal_places=2, max_digits=20)),
                ('products', models.ManyToManyField(to='rep.Product')),
            ],
        ),
    ]
