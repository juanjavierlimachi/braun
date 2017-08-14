# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inicio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='antecedentes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asunto', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('fecha_registro', models.DateTimeField(auto_now=True)),
                ('estado', models.BooleanField(default=True)),
                ('alumno', models.ForeignKey(to='inicio.Alumnos')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
