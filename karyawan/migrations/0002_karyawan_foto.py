# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karyawan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='karyawan',
            name='foto',
            field=models.ImageField(upload_to='C:\\Users\\marcoLC\\Documents\\PythonProject\\mini_hrd\\assets/upload', blank=True),
        ),
    ]
