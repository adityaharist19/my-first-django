# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karyawan', '0001_initial'),
        ('kehadiran', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Izin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_kehadiran', models.CharField(max_length=20, choices=[('izin', 'Izin'), ('cuti', 'Cuti')])),
                ('waktu_mulai', models.DateField()),
                ('waktu_berhenti', models.DateField()),
                ('alasan', models.TextField()),
                ('disetujui', models.BooleanField(default=False)),
                ('karyawan', models.ForeignKey(to='karyawan.Karyawan')),
            ],
        ),
    ]
