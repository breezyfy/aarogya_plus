# Generated by Django 4.2.5 on 2024-03-31 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_doctor_id_doctor_d_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('Apt_no', models.AutoField(primary_key=True, serialize=False)),
                ('time_slot', models.CharField(max_length=100)),
                ('problem', models.TextField()),
            ],
        ),
    ]