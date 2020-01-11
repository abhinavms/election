# Generated by Django 2.2.5 on 2019-10-08 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('admission_no', models.IntegerField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='Candidates')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('All', 'All'), ('R', 'Computer Science'), ('T', 'Electronics And Communication'), ('M', 'Mechanical'), ('A', 'Mechanical Automobile'), ('P', 'Mechanical Production'), ('B', 'Bio Technology')], default='All', max_length=5)),
                ('year', models.IntegerField(choices=[(0, 'All'), (1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], default=0)),
                ('sex', models.CharField(choices=[('All', 'All'), ('M', 'Male'), ('F', 'Female')], default='All', max_length=5)),
                ('degree', models.CharField(choices=[('All', 'All'), ('B', 'B-Tech'), ('M', 'M-Tech')], default='All', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=0)),
                ('admission_no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='poll.Candidate')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Position'),
        ),
    ]
