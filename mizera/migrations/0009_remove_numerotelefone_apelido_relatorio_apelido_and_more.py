# Generated by Django 5.0.4 on 2024-07-09 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mizera', '0008_remove_relatorio_apelido_numerotelefone_apelido_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='numerotelefone',
            name='apelido',
        ),
        migrations.AddField(
            model_name='relatorio',
            name='apelido',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Apelido'),
        ),
        migrations.AlterField(
            model_name='numerotelefone',
            name='numero',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
