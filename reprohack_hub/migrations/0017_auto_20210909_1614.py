# Generated by Django 3.1.4 on 2021-09-09 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reprohack_hub', '0016_auto_20210909_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='archive',
            field=models.BooleanField(default=False, help_text='The paper will no longer be available for review', verbose_name='Archive Paper'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='review_availability',
            field=models.CharField(choices=[('ALL', 'Available for review at any event'), ('EVT_ONLY', 'Only available for review at associated event')], default='ALL', max_length=20, verbose_name='Paper review permission'),
        ),
    ]
