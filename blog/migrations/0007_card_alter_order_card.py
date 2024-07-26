# Generated by Django 5.0.6 on 2024-07-24 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_booking_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('owner_fullname', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.card'),
        ),
    ]
