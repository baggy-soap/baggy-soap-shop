# Generated by Django 2.2.10 on 2020-06-05 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0003_auto_20181115_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='weightbased',
            name='send_multiples',
            field=models.BooleanField(default=False, help_text='Send as multiple packages if the upper weight limit is exceeded', verbose_name='Send Multiples'),
        ),
    ]