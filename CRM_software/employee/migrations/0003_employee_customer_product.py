# Generated by Django 2.1.5 on 2019-03-03 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20190303_0010'),
        ('employee', '0002_auto_20190302_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_customer',
            name='product',
            field=models.ForeignKey(default='-1', on_delete=django.db.models.deletion.CASCADE, to='manager.Product'),
        ),
    ]
