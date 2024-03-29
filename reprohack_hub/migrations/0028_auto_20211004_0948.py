# Generated by Django 3.1.4 on 2021-10-04 09:48

from django.db import migrations, models
import django.db.models.deletion
import reprohack_hub.models


class Migration(migrations.Migration):

    dependencies = [
        ('reprohack_hub', '0027_auto_20211002_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='event',
            field=models.ForeignKey(blank=True, help_text='Is the review associated with an Event? (leave blank if not)', limit_choices_to=reprohack_hub.models.limit_review_event_choices, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reprohack_hub.event'),
        ),
    ]
