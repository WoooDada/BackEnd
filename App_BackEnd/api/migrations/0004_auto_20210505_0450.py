# Generated by Django 3.2 on 2021-05-04 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_account_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uid', models.EmailField(default='', max_length=100, primary_key=True, serialize=False, unique=True)),
                ('nickname', models.CharField(default='', max_length=100, unique=True)),
                ('password', models.CharField(default='', max_length=100)),
                ('birth', models.DateField(null=True, verbose_name='Birth')),
                ('tot_concent_hour', models.IntegerField(default=0, null=True, verbose_name='Total Study Hour')),
                ('sex', models.CharField(choices=[('M', '남성(Man)'), ('W', '여성(Woman)'), ('N', '설정안함(None)')], max_length=1, null=True)),
                ('badge', models.CharField(choices=[('B', 'BRONZE'), ('S', 'SILVER'), ('G', 'GOLD'), ('P', 'PLATINUM'), ('D', 'DIAMOND')], default='B', max_length=2, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
