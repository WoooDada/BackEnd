# Generated by Django 3.2 on 2021-05-11 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_user_user'),
        ('tdl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weekly_tdl',
            fields=[
                ('w_todo_id', models.IntegerField(primary_key=True, serialize=False)),
                ('w_date', models.DateField()),
                ('w_content', models.TextField(max_length=100)),
                ('w_check', models.BooleanField()),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Weekly_tdl_uid', to='api.user')),
            ],
        ),
    ]
