# Generated by Django 4.2.5 on 2024-04-06 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_rename_apt_id_appointment_apt_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('pay_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('pay_type', models.CharField(max_length=20)),
                ('cardcheck_no', models.CharField(max_length=50)),
                ('d', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_d', to='app.doctor')),
                ('p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient')),
                ('s', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_s', to='app.doctor')),
            ],
        ),
    ]
