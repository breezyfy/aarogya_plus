# Generated by Django 4.2.5 on 2024-04-05 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_apt_no_appointment_apt_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='Apt_id',
            new_name='apt_id',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='doc_name',
            new_name='doc',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='pat_name',
            new_name='pat',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='service',
            new_name='serv',
        ),
    ]
