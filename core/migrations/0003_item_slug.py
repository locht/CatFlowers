# Generated by Django 3.0.7 on 2020-08-01 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200801_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]