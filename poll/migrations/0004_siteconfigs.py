# Generated by Django 3.0.2 on 2020-01-12 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0003_candidate_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfigs',
            fields=[
                ('key', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
    ]
