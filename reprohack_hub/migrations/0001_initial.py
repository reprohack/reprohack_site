# Generated by Django 3.1.4 on 2021-04-26 17:32

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import markdownx.models
import reprohack_hub.models
import taggit.managers
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name of User')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('affiliation', models.CharField(blank=True, max_length=70)),
                ('location', models.CharField(blank=True, max_length=70)),
                ('twitter', models.CharField(blank=True, max_length=15)),
                ('github', models.CharField(blank=True, max_length=39)),
                ('orcid', models.CharField(blank=True, max_length=17)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuthorsAndSubmitters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.BooleanField(default=True)),
                ('author', models.BooleanField(default=True)),
                ('submitted', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200, verbose_name='Event Title')),
                ('start_time', models.DateTimeField(default=reprohack_hub.models.default_event_start)),
                ('end_time', models.DateTimeField(default=reprohack_hub.models.default_event_end)),
                ('time_zone', timezone_field.fields.TimeZoneField(default='Europe/London')),
                ('description', markdownx.models.MarkdownxField(verbose_name='Venue description (eg. entrance, parking etc.)')),
                ('location', models.CharField(max_length=200)),
                ('address1', models.CharField(max_length=200)),
                ('address2', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(max_length=60)),
                ('postcode', models.CharField(max_length=15)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('registration_url', models.URLField()),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Paper Title')),
                ('available', models.BooleanField(default=True, verbose_name='Allow for review in any events')),
                ('citation_txt', models.TextField(max_length=300)),
                ('doi', models.CharField(max_length=200, verbose_name='DOI (eg. 10.1000/xyz123)')),
                ('description', models.TextField(max_length=400)),
                ('why', models.TextField(max_length=400)),
                ('focus', models.TextField(max_length=400)),
                ('paper_url', models.URLField()),
                ('code_url', models.URLField()),
                ('data_url', models.URLField()),
                ('extra_url', models.URLField()),
                ('citation_bib', models.TextField()),
                ('public', models.BooleanField(default=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(blank=True, default=False, verbose_name='Removed from any reviews')),
                ('authors_and_submitters', models.ManyToManyField(through='reprohack_hub.AuthorsAndSubmitters', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reprohack_hub.event')),
                ('tools', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='PaperReviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead_reviewer', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reproducibility_outcome', models.CharField(choices=[('y', 'Fully Reproducible'), ('p', 'Partially Reproducible'), ('n', 'Not Reproducible')], default='n', max_length=1, verbose_name='Did you manage to reproduce it?')),
                ('reproducibility_rating', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='How much of the paper did you manage to reproduce?')),
                ('reproducibility_description', models.TextField(verbose_name='Briefly describe the procedure followed/tools used to reproduce it.')),
                ('familiarity_with_method', models.TextField(verbose_name='Briefly describe your familiarity with the procedure/tools used by the paper.')),
                ('operating_system', models.CharField(choices=[('linux', 'Linux/FreeBSD or other Open Source Operating system'), ('macOS', 'Apple Operating System'), ('windows', 'Windows Operating System')], max_length=7, verbose_name='Which type of operating system were you working in?')),
                ('operating_system_detail', models.CharField(max_length=100, verbose_name='What operating system were you using (eg. Ubuntu 14.04.6 LTS, macOS 10.15 or Windows 10 Pro)?')),
                ('software_installed', models.TextField(verbose_name='What additional software did you need to install?')),
                ('software_used', models.TextField(verbose_name='What software did you use?')),
                ('challenges', models.TextField(verbose_name='What were the main challenges you ran into (if any)?')),
                ('advantages', models.TextField(verbose_name='What were the positive features of this approach?')),
                ('comments_and_suggestions', models.TextField(verbose_name='Any other comments/suggestions on the reproducibility approach?')),
                ('documentation_rating', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='How well was the material documented?')),
                ('documentation_cons', models.TextField(verbose_name='How could the documentation be improved?')),
                ('documentation_pros', models.TextField(verbose_name='What do you like about the documentation?')),
                ('method_familiarity_rating', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='After attempting to reproduce, how familiar do you feel with the code and methods used in the paper?')),
                ('transparency_suggestions', models.TextField(verbose_name='Any suggestions on how the analysis could be made more transparent?')),
                ('method_reusability_rating', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Rate the project on reusability of the material.')),
                ('data_permissive_license', models.BooleanField(verbose_name='Permissive license for DATA included')),
                ('code_permissive_license', models.BooleanField(verbose_name='Permissive license for CODE included')),
                ('reusability_suggestions', models.TextField(verbose_name='Any suggestions on how the project could be more reusable?')),
                ('general_comments', models.TextField(verbose_name='Any final comments:')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reprohack_hub.event')),
                ('paper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reprohack_hub.paper')),
                ('reviewers', models.ManyToManyField(through='reprohack_hub.PaperReviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paperreviewer',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reprohack_hub.review'),
        ),
        migrations.AddField(
            model_name='paperreviewer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='authorsandsubmitters',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reprohack_hub.paper'),
        ),
        migrations.AddField(
            model_name='authorsandsubmitters',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]