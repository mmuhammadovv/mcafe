# Generated by Django 5.0.6 on 2024-07-12 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='img',
            field=models.ImageField(default=11, upload_to='team'),
            preserve_default=False,
        ),
    ]
