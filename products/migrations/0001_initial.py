<<<<<<< HEAD
# Generated by Django 4.0.1 on 2022-02-07 08:28
=======
# Generated by Django 4.0.1 on 2022-01-31 18:43
>>>>>>> e4d43012ba5cfe4b8fb8d5787b210d8d221fa386

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeyIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'key_ingredients',
            },
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'main_categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('ingredients_etc', models.TextField()),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Skintype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'skintypes',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField()),
                ('main_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.maincategory')),
            ],
            options={
                'db_table': 'sub_categories',
            },
        ),
        migrations.CreateModel(
            name='ProductUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dosage', models.CharField(blank=True, max_length=250)),
                ('texture', models.CharField(blank=True, max_length=100)),
                ('aroma', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(max_length=250, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_usages', to='products.product')),
            ],
            options={
                'db_table': 'products_usages',
            },
        ),
        migrations.CreateModel(
            name='ProductSkintype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_skin_type', to='products.product')),
<<<<<<< HEAD
                ('skin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skin_type', to='products.skintype')),
=======
                ('skin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.skintype')),
>>>>>>> e4d43012ba5cfe4b8fb8d5787b210d8d221fa386
            ],
            options={
                'db_table': 'products_skintypes',
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('size', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=3, default=0, max_digits=9, null=True)),
                ('stock', models.PositiveIntegerField(default=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_options', to='products.product')),
            ],
            options={
                'db_table': 'products_options',
            },
        ),
        migrations.CreateModel(
            name='ProductIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
<<<<<<< HEAD
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_ingredient', to='products.keyingredient')),
=======
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_id', to='products.keyingredient')),
>>>>>>> e4d43012ba5cfe4b8fb8d5787b210d8d221fa386
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_key_ingredient', to='products.product')),
            ],
            options={
                'db_table': 'products_ingredients',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.subcategory'),
        ),
    ]
