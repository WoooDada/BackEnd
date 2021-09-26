# Generated by Django 2.2 on 2021-09-26 05:06

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_user_image'),
        ('main', '0006_auto_20210925_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room_enroll',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='room_enroll',
            name='start_date',
        ),
        migrations.CreateModel(
            name='Recent_Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_array', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=models.CharField(max_length=10)), size=None)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
        ),
    ]