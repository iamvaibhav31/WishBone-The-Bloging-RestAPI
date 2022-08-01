# Generated by Django 3.2.8 on 2022-04-06 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('auth_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='email_validator',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('is_varified', models.BooleanField(default=False)),
            ],
        ),
    ]
