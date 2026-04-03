# Generated migration - Fixed dependencies

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onehub_app', '0009_hotel_hotelname'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ecommerce_admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='onehub_app.ecommerceadmin'),
            preserve_default=False,
        ),
    ]
