# Generated by Django 3.2.8 on 2021-10-24 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rep', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentproject',
            name='number_of_apartments',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='investmentproject',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='investmentproject',
            name='city',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='investmentproject',
            name='district',
            field=models.CharField(choices=[('center area', 'center area'), ('sub urban', 'sub urban'), ('business district', 'business district'), ('midtown', 'midtown'), ('outer center area', 'outer center area')], max_length=64),
        ),
        migrations.AlterField(
            model_name='investmentproject',
            name='finnish_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='investmentproject',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='investmentproject',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
