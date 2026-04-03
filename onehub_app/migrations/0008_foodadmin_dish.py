# Generated migration file for Food Delivery models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onehub_app', '0007_ecommerceadmin_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=200)),
                ('owner_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('location', models.TextField()),
                ('password', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Food Admin',
                'verbose_name_plural': 'Food Admins',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snacks', 'Snacks'), ('drinks', 'Drinks')], max_length=20)),
                ('food_type', models.CharField(choices=[('veg', 'Veg'), ('non_veg', 'Non-Veg')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dish_image', models.ImageField(upload_to='dishes/')),
                ('availability_status', models.BooleanField(default=True, help_text='True = Available, False = Out of Stock')),
                ('is_available_now', models.BooleanField(default=True, help_text='True = Available Now, False = Not Available Now')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('food_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='onehub_app.foodadmin')),
            ],
            options={
                'verbose_name': 'Dish',
                'verbose_name_plural': 'Dishes',
                'ordering': ['-created_at'],
            },
        ),
    ]
