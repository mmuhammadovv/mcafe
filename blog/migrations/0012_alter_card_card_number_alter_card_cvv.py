# Generated by Django 5.0.6 on 2024-07-25 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_card_card_number_alter_card_cvv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.IntegerField(max_length=16),
        ),
        migrations.AlterField(
            model_name='card',
            name='cvv',
            field=models.IntegerField(max_length=3),
        ),
    ]