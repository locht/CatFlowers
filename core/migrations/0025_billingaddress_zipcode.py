# Generated by Django 3.0.7 on 2020-08-02 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_billingaddress_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='zipcode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
