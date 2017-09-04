# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0003_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnos',
            name='curso',
            field=models.ForeignKey(default=1, to='inicio.Curso'),
            preserve_default=False,
        ),
    ]
