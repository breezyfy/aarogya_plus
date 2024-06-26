# Generated by Django 4.2.5 on 2024-04-05 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_appointment_apt_date_appointment_dept'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='Apt_no',
            new_name='Apt_id',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='dept',
        ),
        migrations.AddField(
            model_name='appointment',
            name='pat_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.patient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_service', to='app.doctor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doc_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_doc', to='app.doctor'),
        ),
    ]
