# Generated by Django 5.0.6 on 2024-06-07 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(default='Título por defecto', max_length=100),
        ),
    ]
