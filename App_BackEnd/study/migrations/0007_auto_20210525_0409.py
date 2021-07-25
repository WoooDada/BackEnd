# Generated by Django 3.2 on 2021-05-25 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_user_user'),
        ('study', '0006_one_week_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='One_week_study_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10, null=True)),
                ('concent_time', models.IntegerField(default=0, null=True)),
                ('play_time', models.IntegerField(default=0, null=True)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one_week_uid', to='api.user')),
            ],
        ),
        migrations.DeleteModel(
            name='One_week_data',
        ),
    ]