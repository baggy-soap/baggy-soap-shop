# Generated by Django 2.2.10 on 2020-08-05 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20181115_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='package_count',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Package count'),
        ),
    ]
