# Generated by Django 3.1.4 on 2021-09-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reprohack_hub', '0012_auto_20210907_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='operating_system',
            field=models.CharField(choices=[('linux', 'Linux/FreeBSD or other Open Source Operating system'), ('macOS', 'Apple Operating System (macOS)'), ('windows', 'Windows Operating System')], max_length=7, verbose_name='Which type of operating system were you working in?'),
        ),
    ]
