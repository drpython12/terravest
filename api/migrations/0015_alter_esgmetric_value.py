# Generated by Django 5.1.1 on 2025-04-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_esgcompany_isin_alter_esgcompany_siccode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esgmetric',
            name='value',
            field=models.TextField(),
        ),
    ]
