# Generated by Django 4.2.5 on 2024-03-31 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_patient_id_patient_p_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='id',
        ),
        migrations.AddField(
            model_name='doctor',
            name='d_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
