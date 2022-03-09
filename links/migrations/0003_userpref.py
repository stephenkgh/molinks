# Generated by Django 4.0.3 on 2022-03-07 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('links', '0002_alter_category_options_alter_link_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('theme', models.CharField(choices=[('MO', 'Maureen'), ('NE', 'L33t NeRD'), ('DA', 'Darkness'), ('BO', 'All Business')], max_length=2)),
            ],
        ),
    ]