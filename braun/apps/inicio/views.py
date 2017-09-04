#encoding:utf-8
from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, context
from django.contrib.auth.forms import User
from .forms import *#aki estoy importando todos mis formularios de mi achivo form.py
from .models import *##aki estoy importando todos mis models de mi achivo models.py
# Create your views here.
from django.views.generic import TemplateView, FormView,ListView,CreateView
from django.core.urlresolvers import reverse_lazy
import datetime
import calendar
from django.db.models import Q
import StringIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from datetime import datetime, date, time, timedelta

# Create your views here.
def inicio(request):
	return render(request,'inicio/inicio.html')

def loguin(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado/')
	if request.method=='POST':
		print "has escho POST"
		formulario=AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario=request.POST['name']
			print usuario
			clave=request.POST['password']
			print clave
			acceso=authenticate(username=usuario,password=clave)
			if acceso is not None:
				if acceso.is_superuser:
					login(request,acceso)
					return HttpResponse('/privado/')
				else:
					if acceso.is_staff:
						login(request,acceso)
						return HttpResponse('/privado/')
					else:
						if acceso.is_active:
							login(request,acceso)
							return HttpResponseRedirect('/privado/')
						else:
							return HttpResponse("Error, Usuario o contraseña incorrecta.")
			else:
				return HttpResponse("Error, Usuario o contraseña incorrecta.")
	else:
		formulario=AuthenticationForm()
	return render(request,'inicio/loguin.html')
@login_required(login_url='/')
def privado(request):
	now = datetime.now()
	if request.user.is_superuser:
		return render(request,'administrador/admin.html',{'now':now},context_instance=RequestContext(request))
	else:
		#user.is_staff decimoe q el administrador le dio el permiso para subsustema secretria
		if request.user.is_staff:
			return render(request,'administrador/admin.html',{'now':now},context_instance=RequestContext(request))
		else:
			if request.user.is_active:
				return render(request,'inicio/inicio.html',{'now':now},context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/salir/')

@login_required(login_url='/')
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/')
def editar_perfil(request):
	if request.method=='POST':
		user_form=UserForms(request.POST,instance=request.user)
		#perfil_form=formPerfiles(request.POST,instance=request.user.perfilDirector)
		try:
			perfil_form=formPerfiles(request.POST,instance=request.user.perfilDirector)
			print "Director: ",perfil_form
			if user_form.is_valid() and perfil_form.is_valid():
				user_form.save()
				perfil_form.save()
				return HttpResponse("Actualizaste tus Datos correctamente.")
		except:
			perfil_form=formPerfiles(request.POST,instance=request.user.perfil)
			if user_form.is_valid() and perfil_form.is_valid():
				user_form.save()
				perfil_form.save()
				return HttpResponse("Actualizaste tu Datos correctamente.")
	else:
		user_form=UserForms(instance=request.user)
		perfil_form=""
		try:
			perfil_form=formPerfiles(instance=request.user.perfilDirector)
		except:
			perfil_form=formPerfiles(instance=request.user.perfil)
	return render_to_response('inicio/datosPerfil.html',{'user_form':user_form,'perfil_form':perfil_form},context_instance=RequestContext(request))
class nuevoUser(FormView):
	template_name = 'inicio/nuevo.html'
	form_class=UserForm
	success_url = reverse_lazy('listaUsuarios')
	def form_valid(self,form):
		user=form.save()
		perfil=Perfiles()
		perfil.usuario = user
		perfil.materno=form.cleaned_data['materno']
		perfil.ci=form.cleaned_data['ci']
		perfil.telefono=form.cleaned_data['telefono']
		perfil.save()
		return super(nuevoUser, self).form_valid(form)

class nuevoDirector(FormView):
	template_name = 'administrador/nuevoDirector.html'
	form_class=UserFormDirector
	success_url = reverse_lazy('verDitectores')
	def form_valid(self,form):
		user=form.save()
		perfil=Directores()
		perfil.usuario = user
		perfil.materno=form.cleaned_data['materno']
		perfil.ci=form.cleaned_data['ci']
		perfil.telefono=form.cleaned_data['telefono']
		perfil.save()
		return super(nuevoDirector, self).form_valid(form)

######hacer una consulta para optener todos los cursos
class nuevoAlumno(FormView):
	template_name = 'administrador/nuevoAlumno.html'
	form_class=UserFormAlumno
	success_url = reverse_lazy('verAlumno')
	def form_valid(self,form):
		user=form.save()
		perfil=Alumnos()
		perfil.usuario = user
		perfil.materno=form.cleaned_data['materno'].capitalize()
		#perfil.curso.form.cleaned_data['curso']
		perfil.ci=form.cleaned_data['ci']
		perfil.telefono=form.cleaned_data['telefono']
		perfil.save()
		return super(nuevoAlumno, self).form_valid(form)

def nuevoAlumnoA(request):
	cursos = Curso.objects.all()
	print "principal"
	if request.method=="POST":
		form=Alumnoforms(request.POST)
		if(form.is_valid()):
			alumno=User()
			alumno.password=request.POST['password']
			alumno.username=request.POST['username']
			alumno.first_name=request.POST['first_name']
			alumno.last_name=request.POST['last_name']
			alumno.email=request.POST['email']
			alumno.save()
			#form.save()
			objeto = alumno.save()
			print "ultimo id Registrado",alumno.id
			perfil=Alumnos()
			perfil.usuario_id = alumno.id
			perfil.materno=request.POST['materno']
			perfil.curso_id=int(request.POST['curso'])
			perfil.ci=int(request.POST['ci'])
			perfil.telefono=int(request.POST['telefono'])

			perfil.save()
			return HttpResponseRedirect("/escogido/%s/"%(alumno.id))
	form=Alumnoforms()
	Perfil = formPerfil()
	return render_to_response('administrador/nuevoAlumno.html',{"form":form,'Perfil':Perfil,'cursos':cursos},RequestContext(request))
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def verHistoriales(request):
	historiales = antecedentes.objects.filter(estado=True).order_by("-id")
	t_his = antecedentes.objects.filter(estado=True).count()
	alumnos = Alumnos.objects.all().order_by("-id")
	usuarios = User.objects.filter(is_active=True).order_by("-id")
	cursos=Curso.objects.filter(estado=True)
	paginator=Paginator(historiales,20)
	page = request.GET.get('page')
	try:
		contenido = paginator.page(page)
	except PageNotAnInteger:
		contenido = paginator.page(1)
	except EmptyPage:
		contenido = paginator.page(paginator.num_pages)
	return render_to_response('administrador/verHistorial.html',{'cursos':cursos,'alumnos':alumnos,'usuarios':usuarios,'contenido':contenido,'historiales':contenido,'t_his':t_his},context_instance=RequestContext(request))
def verDitectores(request):
	users=User.objects.all().order_by("-id")
	perfil=Directores.objects.all().order_by("-id")
	t_user=Directores.objects.all().count()
	return render_to_response("administrador/DatosDirectores.html",{'users':users,'perfil':perfil,'t_user':t_user},context_instance=RequestContext(request))

def verAlumno(request):
	users=User.objects.filter(is_staff=False,is_superuser=False).order_by("-id")
	t_user=User.objects.filter(is_staff=False,is_superuser=False).count()
	paginator=Paginator(users,20)
	page = request.GET.get('page')
	try:
		contenido = paginator.page(page)
	except PageNotAnInteger:
		contenido = paginator.page(1)
	except EmptyPage:
		contenido = paginator.page(paginator.num_pages)
	return render_to_response("administrador/verAlumno.html",{'users':contenido,'contenido':contenido,'t_user':t_user},context_instance=RequestContext(request))
def DatosUsuario(request):
	users=User.objects.all().order_by("-id")
	perfil=Perfiles.objects.all().order_by("-id")
	t_user=Perfiles.objects.all().count()
	return render_to_response("inicio/DatosUsuario.html",{'users':users,'perfil':perfil,'t_user':t_user},context_instance=RequestContext(request))
def verificacion(request):
	use=request.GET['use']
	try:
		us=User.objects.get(username=use)
		return HttpResponse("El Nombre de Usuario %s, ya existe Intente con otro Nombre."%(us))
	except User.DoesNotExist:
		return HttpResponse()
def PlanBimestral(request):
	if request.method=='POST':
		Usuario=Bismestre(docente=request.user)
		forms = FormBimestre(request.POST,request.FILES,instance=Usuario)
		if forms.is_valid():
			forms.save()
			message = "Los datos de registraron correctamente!"
	else:
		forms = FormBimestre()
	return render(request,'inicio/PlanBimestral.html',{'forms':forms},context_instance=RequestContext(request))
def newAvanse(request):
	if request.method=="POST":
		Usuario=Avanse(docente=request.user)
		forms = FormAvanse(request.POST,request.FILES,instance=Usuario)
		if forms.is_valid():
			forms.save()
			message = "Los datos de registraron correctamente!"
	else:
		forms = FormAvanse()
	return render(request,'inicio/newAvanse.html',{'forms':forms},context_instance=RequestContext(request))

def verPlanBimestral(request):
	bimestres = Bismestre.objects.all().order_by("-id")
	t_b = Bismestre.objects.all().count()
	return render(request,'inicio/verPlanBimestral.html',{'bimestres':bimestres,'t_b':t_b},context_instance=RequestContext(request))
def verAvances(request):
	avanses = Avanse.objects.all().order_by("-id")
	t_a = Avanse.objects.all().count()
	return render(request,'inicio/verAvances.html',{'avanses':avanses,'t_a':t_a},context_instance=RequestContext(request))
def docentes(request):
	director=User.objects.filter(is_superuser=True).order_by("-id")
	dire=Directores.objects.all().order_by("-id")[0:1]
	for i in director:
		for j in dire:
			if j.usuario.id == i.id:
				print "director:",i.username
				break
	return render(request, 'inicio/docentes.html',{'director':director,'dire':dire})

def generar_pdf(html):
	resultado=StringIO.StringIO()
	pdf=pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")),resultado)
	if not pdf.err:
		return HttpResponse(resultado.getvalue(),'application/pdf')
	return HttpResponse("Error al generar el reporte")

def imprimirHistorial(request,id):
	histo = antecedentes.objects.filter(alumno=int(id),estado=True).order_by("-id")[0:1]
	print histo
	if len(histo)>0:
		h=""
		for i in histo:
			h=i.id
			print "hoofofg",h
			break
		datos = antecedentes.objects.get(id=int(h))
		print "daot alumno",datos.alumno
		nombre_alumno = User.objects.get(username=datos.alumno)
	else:
		return HttpResponse("No se Registró ningún historial para este alumno")
	#print nombre_alumno.get_full_name
	fecha = datetime.now()
	fecha="%s/%s/%s" % (fecha.day,fecha.month,fecha.year)
	html=render_to_string('inicio/imprimirHistorial.html',{'datos':datos,'fecha':fecha,'nombre_alumno':nombre_alumno},context_instance=RequestContext(request))
	return generar_pdf(html)

def Informacion(request, id):
	dato=Bismestre.objects.get(id=int(id))
	return render(request, 'inicio/Informacion.html',{'dato':dato},context_instance=RequestContext(request))
def NewAnteRegistro(request):
	if request.method == 'POST':
		usuario=antecedentes(usuario=request.user)
		forms = FormAnte(request.POST,instance=usuario)
		if forms.is_valid():
			forms.save()
			return HttpResponse("Historial Registrado correctamente.")
	else:
		forms = FormAnte()
	return render(request,'inicio/NewAnteRegistro.html',{'forms':forms},context_instance=RequestContext(request))
def NewAntecedente(request):
	return render(request,'inicio/NewAntecedente.html')
def buscarAlumno(request):
	if request.method=="POST":
		texto=request.POST["alumno"]
		busqueda=(
			Q(first_name__icontains=texto) |
			Q(last_name__icontains=texto) |
			Q(username__icontains=texto)
		)
		resultados=User.objects.filter(busqueda, is_active=True).distinct()
		return render_to_response('inicio/buscarAlumno.html',{'resultados':resultados},context_instance=RequestContext(request))
	else:
		texto=request.GET["alumno"]
		busqueda=(
			Q(first_name__icontains=texto) |
			Q(last_name__icontains=texto) |
			Q(username__icontains=texto)
		)
		resultados=User.objects.filter(busqueda, is_active=True).distinct()
		return render_to_response('inicio/buscarAlumno.html',{'resultados':resultados},context_instance=RequestContext(request))	
def buscar(request):
	if request.method=="POST":
		texto=request.POST["q"]
		busqueda=(
			Q(id__icontains=texto) |
			Q(id__icontains=texto) |
			Q(id__icontains=texto)
		)
		resultados=antecedentes.objects.filter(busqueda).distinct()
		uu=""
		for i in resultados:
			uu=i.alumno.ci
			break
		try:
			alumno=User.objects.get(username=uu)
		except User.DoesNotExist:
			return HttpResponse("Registro no Encontrado :(")
		print "User Alumno",alumno
		return render_to_response('inicio/buscarHistorial.html',{'resultados':resultados,'alumno':alumno},context_instance=RequestContext(request))

def escogido(request,id):
	user = User.objects.get(id=int(id))
	if request.method == 'POST':
		usuario = request.user.id
		alumno = user.perfilAlumno.id
		forms = FormAnte(request.POST)
		if forms.is_valid():
			antecedente=antecedentes()
			antecedente.usuario_id = int(usuario)
			antecedente.alumno_id = int(alumno)
			antecedente.asunto = request.POST['asunto']
			antecedente.descripcion = request.POST['descripcion']
			antecedente.save()
			return HttpResponse("Historial Registrado correctamente.")
		else:
			return HttpResponse("Error complete los datos")
	else:
		forms = FormAnte()
	return render(request,'inicio/escogido.html',{'users':user,'forms':forms},context_instance=RequestContext(request))
def VerAntecedente(request, id):
	datos = antecedentes.objects.filter(alumno=int(id)).order_by("-id")[0:1]
	print datos
	return render(request,'inicio/VerAntecedente.html',{'datos':datos},context_instance=RequestContext(request))
def verHistorial(request,id):
	today=datetime.now()
	inicio="%s-01-01" % (today.year)
	print inicio
	fecha=datetime.now()
	fin="%s-%s-%s" % (today.year, today.month, calendar.monthrange(today.year-1, today.month-1)[1])
	datos=antecedentes.objects.filter(alumno=int(id),fecha_registro__range=(inicio,fecha)).order_by("-id")
	print fin
	cont=antecedentes.objects.filter(alumno=int(id),fecha_registro__range=(inicio,fecha)).count()
	return render(request,'inicio/VerAntecedente.html',{'datos':datos,'cont':cont},context_instance=RequestContext(request))

def Darbaja(request,id):
	dato=User.objects.get(id=int(id))
	return render(request,'inicio/Darbaja.html',{'dato':dato},context_instance=RequestContext(request))
def DelAlumno(request,id):
	User.objects.filter(id=int(id)).update(is_active=False)
	return HttpResponse("El Alumno se dió de Baja Correctamente.")
def DarAlta(request,id):
	dato=User.objects.get(id=int(id))
	return render(request,'inicio/DarAlta.html',{'dato':dato},context_instance=RequestContext(request))
def AltaAlumno(request,id):
	User.objects.filter(id=int(id)).update(is_active=True)
	return HttpResponse("El Alumno se dió de Alta Correctamente.")
def EditAlumno(request,id):
	dato=User.objects.get(id=int(id))
	perfil=Alumnos.objects.get(usuario=int(id))
	if request.method == 'POST':
		formsUser=FormEditUser(request.POST,instance=dato)
		formsAlum=FormEdirAlum(request.POST,instance=perfil)
		if formsUser.is_valid() and formsAlum.is_valid():
			formsUser.save()
			formsAlum.save()
			User.objects.filter(id=int(id)).update(username=int(request.POST['ci']))
			return HttpResponse("Datos Actualizados Correctamente")
	else:
		formsUser=FormEditUser(instance=dato)
		formsAlum=FormEdirAlum(instance=perfil)
	return render(request,'inicio/EditAlumno.html',{'formsUser':formsUser,'formsAlum':formsAlum,'cod':int(id)},context_instance=RequestContext(request))

def BajaAntecedente(request,id):
	dato=antecedentes.objects.get(id=int(id))
	return render(request,'inicio/BajaAntecedente.html',{'dato':dato},context_instance=RequestContext(request))
def DelAntecedentes(request,id):
	antecedentes.objects.filter(id=int(id)).update(estado=False)
	return HttpResponse("La Información se dió de Baja Correctamente.")
def AltaAntecedente(request, id):
	dato=antecedentes.objects.get(id=int(id))
	return render(request,'inicio/AltaAntecedente.html',{'dato':dato},context_instance=RequestContext(request))
def editAnte(request,id):
	dato=antecedentes.objects.get(id=int(id))
	if request.method=="POST":
		forms=FormAnte(request.POST,instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("Información actualizada Correctamente")
	else:
		forms=FormAnte(instance=dato)
	return render(request,'inicio/editAnte.html',{'forms':forms,'dato':dato},context_instance=RequestContext(request))
def bajaAntecendetes(request, id):
	antecedentes.objects.filter(id=int(id)).update(estado=True)
	return HttpResponse("La Información se dió de Alta Correctamente.")

def DarbajaDocente(request,id):
	dato=User.objects.get(id=int(id))
	return render(request,'inicio/DarbajaDocente.html',{'dato':dato},context_instance=RequestContext(request))
def Deletedocente(request, id):
	User.objects.filter(id=int(id)).update(is_staff=False)
	return HttpResponse("El Profesor se dió de Baja Correctamente.")
def DarAltaDocente(request, id):
	dato=User.objects.get(id=int(id))
	return render(request,'inicio/DarAltaDocente.html',{'dato':dato},context_instance=RequestContext(request))
def Altadocentes(request, id):
	User.objects.filter(id=int(id)).update(is_staff=True)
	return HttpResponse("El Profesor se dió de Alta Correctamente.")
def Canbiodirector(request,id):
	User.objects.filter(id=int(id)).update(is_superuser=False)
	return HttpResponse("Por razones de seguridad su cuenta se ha dado de bajo,<br>Ingrese con la cuenta del nuevo director.")
def por_curso(request):
	id_curso = request.GET['id']
	alumnos = Alumnos.objects.filter(curso_id=int(id_curso)).distinct().order_by("-id")
	today=datetime.now()
	inicio="%s-01-01" % (today.year)
	fecha=datetime.now()
	historiales = antecedentes.objects.filter(estado=True,fecha_registro__range=(inicio,fecha)).order_by("-id")
	#t_his = antecedentes.objects.filter(estado=True).count()#no muestra el total de registros por curso
	usuarios = User.objects.filter(is_active=True).order_by("-id")
	cursos=Curso.objects.get(id=int(id_curso))
	contador = 0
	for j in historiales:
		for i in alumnos:
			for k in usuarios:	
				if j.alumno.id == i.id and i.usuario.id == k.id:
					contador=contador +1

	dic={
		'alumnos':alumnos,
		'historiales':historiales,
		't_his':contador,
		'usuarios':usuarios,
		'cursos':cursos,
	}
	return render(request,'administrador/por_curso.html',dic,context_instance=RequestContext(request))