# Generated by Django 4.0 on 2022-06-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profil_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
