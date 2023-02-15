# Generated by Django 4.1.6 on 2023-02-15 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_item_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='время создания')),
                ('item', models.ManyToManyField(related_name='item', to='orders.item', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
                'ordering': ('-datetime_created',),
            },
        ),
    ]
