# Generated by Django 5.0.6 on 2024-07-12 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('exprience', models.IntegerField()),
                ('social_nicknam', models.CharField(max_length=50)),
            ],
        ),
    ]