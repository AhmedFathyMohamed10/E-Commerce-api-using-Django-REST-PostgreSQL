# Generated by Django 4.1.13 on 2024-06-11 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(related_name='orders', to='order.order'),
        ),
    ]
