# Generated by Django 5.0.6 on 2024-07-24 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_order_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='cvv',
            field=models.IntegerField(default=1, max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.IntegerField(max_length=16),
        ),
    ]
