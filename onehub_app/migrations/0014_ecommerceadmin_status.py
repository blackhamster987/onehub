# Generated migration to add status field to EcommerceAdmin

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onehub_app', '0013_product_ecommerce_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecommerceadmin',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                default='pending'
            ),
        ),
    ]
