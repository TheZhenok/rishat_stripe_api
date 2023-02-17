# Generated by Django 4.1.6 on 2023-02-17 08:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_item_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ManyToManyField(related_name='order', to='orders.item', verbose_name='товар'),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_ending', models.DateTimeField(verbose_name='время завершения скидки')),
                ('persent', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='размер скидки')),
                ('item', models.ManyToManyField(related_name='discont', to='orders.item', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'скидка',
                'verbose_name_plural': 'скидки',
                'ordering': ('-datetime_ending',),
            },
        ),
    ]