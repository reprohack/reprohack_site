# Generated by Django 3.1.4 on 2021-10-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reprohack_hub', '0029_auto_20211004_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='public_reviews',
            field=models.BooleanField(default=True, help_text='Only reviews that have also been set to public by reviewers will be visible to other signed in users', verbose_name='Make reviews public'),
        ),
    ]