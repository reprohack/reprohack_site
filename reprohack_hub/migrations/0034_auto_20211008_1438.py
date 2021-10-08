# Generated by Django 3.1.4 on 2021-10-08 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reprohack_hub', '0033_auto_20211007_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='code_permissive_license',
            field=models.BooleanField(default=False, verbose_name='Permissive license for CODE included'),
        ),
        migrations.AlterField(
            model_name='review',
            name='data_permissive_license',
            field=models.BooleanField(default=False, verbose_name='Permissive license for DATA included'),
        ),
    ]
