# Generated by Django 5.0.4 on 2024-07-09 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mizera', '0010_alter_numerotelefone_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numerotelefone',
            name='numero',
            field=models.CharField(max_length=11, null=True, unique=True),
        ),
    ]
