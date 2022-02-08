# Generated by Django 4.0.1 on 2022-02-08 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=45)),
                ('receive_letter', models.BooleanField(default=False)),
                ('skintype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.skintype')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nation_code', models.CharField(blank=True, max_length=10)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('address_detail', models.CharField(blank=True, max_length=100)),
                ('post_number', models.CharField(blank=True, max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'addresses',
            },
        ),
    ]
