# Generated by Django 4.2.5 on 2024-03-16 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=100, verbose_name='')),
                ('date_of_birth', models.CharField(max_length=100, verbose_name='')),
                ('age', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=100)),
                ('gender', models.CharField(max_length=50)),
                ('address', models.TextField()),
            ],
        ),
    ]
