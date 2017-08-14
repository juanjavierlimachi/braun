#encoding:utf-8
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.forms import User
# Create your models here.
class Perfiles(models.Model):
	usuario = models.OneToOneField(User, unique=True, related_name='perfil')
	materno = models.CharField(max_length=50)
	ci = models.IntegerField()
	telefono = models.IntegerField()
	def __unicode__(self):
		return self.usuario.username
class Bismestre(models.Model):
	bimestre = models.IntegerField()
	titulo = models.CharField(max_length=50)
	descripcion = models.TextField(blank=True, null=True)
	archivo = models.FileField(upload_to = 'bimestres')
	docente = models.ForeignKey(User)
	fecha_registro=models.DateTimeField(auto_now=True)
	estado = models.BooleanField(default=True)
	def __unicode__(self):
		return self.titulo
class Avanse(models.Model):
	titulo = models.CharField(max_length=50)
	descripcion = models.TextField(blank=True, null=True)
	materia = models.CharField(max_length=50)
	docente = models.ForeignKey(User)
	archivo = models.FileField(upload_to = 'avanses')
	estado = models.BooleanField(default=True)
	fecha_registro=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.titulo
class Alumnos(models.Model):
	usuario = models.OneToOneField(User, unique=True, related_name='perfilAlumno')
	materno = models.CharField(max_length=50)
	ci = models.IntegerField(blank=True,null=True)
	telefono = models.IntegerField(blank=True,null=True)
	def __unicode__(self):
		return "%s"%(self.ci)
class Directores(models.Model):
	usuario = models.OneToOneField(User, unique=True, related_name='perfilDirector')
	materno = models.CharField(max_length=50)
	ci = models.IntegerField()
	telefono = models.IntegerField()
	def __unicode__(self):
		return self.usuario.username
class antecedentes(models.Model):
	usuario=models.ForeignKey(User)
	alumno=models.ForeignKey(Alumnos)
	asunto=models.CharField(max_length=50)
	descripcion=models.TextField()
	fecha_registro=models.DateTimeField(auto_now=True)
	estado=models.BooleanField(default=True)
	def __unicode__(self):
		return self.alumno.materno