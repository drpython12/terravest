# Generated by Django 5.1.1 on 2025-03-15 15:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_portfoliostock'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_type', models.CharField(choices=[('stocks', 'Stocks'), ('bonds', 'Bonds'), ('real_estate', 'Real Estate'), ('crypto', 'Cryptocurrency')], max_length=50)),
                ('risk_level', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('investment_strategy', models.CharField(choices=[('impact_investing', 'Impact Investing'), ('esg_integration', 'ESG Integration'), ('ethical_screening', 'Ethical Screening'), ('traditional_esg', 'Traditional Investing with ESG Consideration')], max_length=50)),
                ('esg_factors', models.JSONField(default=list)),
                ('industry_preferences', models.JSONField(blank=True, default=list)),
                ('exclusions', models.JSONField(blank=True, default=list)),
                ('sentiment_analysis', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=10)),
                ('transparency_level', models.CharField(choices=[('simple_summary', 'Simple Summary'), ('detailed_breakdown', 'Detailed Breakdown')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
