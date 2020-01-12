# Generated by Django 2.2.5 on 2020-01-12 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_siteconfigs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.IntegerField(default=1)),
                ('candidate_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='poll.Candidate')),
            ],
        ),
    ]
