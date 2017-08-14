# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumnos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('materno', models.CharField(max_length=50)),
                ('ci', models.IntegerField(null=True, blank=True)),
                ('telefono', models.IntegerField(null=True, blank=True)),
                ('usuario', models.OneToOneField(related_name='perfilAlumno', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Avanse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('materia', models.CharField(max_length=50)),
                ('archivo', models.FileField(upload_to=b'avanses')),
                ('estado', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now=True)),
                ('docente', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bismestre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bimestre', models.IntegerField()),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('archivo', models.FileField(upload_to=b'bimestres')),
                ('fecha_registro', models.DateTimeField(auto_now=True)),
                ('estado', models.BooleanField(default=True)),
                ('docente', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Directores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('materno', models.CharField(max_length=50)),
                ('ci', models.IntegerField()),
                ('telefono', models.IntegerField()),
                ('usuario', models.OneToOneField(related_name='perfilDirector', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perfiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('materno', models.CharField(max_length=50)),
                ('ci', models.IntegerField()),
                ('telefono', models.IntegerField()),
                ('usuario', models.OneToOneField(related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
