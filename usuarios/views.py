from django.shortcuts import render
from django.shortcuts import redirect
from hashlib import sha256
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

from .models import Usuario



def validar_register(request):
  nome = request.POST.get('nome')
  email = request.POST.get('email')
  senha = request.POST.get('senha')
  matricula = request.POST.get('matricula')
  setor = request.POST.get('setor')

  if len(nome.strip()) == 0 or len(email.strip()) == 0:
    messages.add_message(request,constants.ERROR,"Nome e e-mail devem ser preenchidos.")
    return redirect("/auth/register/")
    # Se o usuário não digitou nada
  if len(senha)<8:
    messages.add_message(request,constants.INFO,"A senha deve conter pelo 8 dígitos")
    return redirect("/auth/register/")
    # Se o usuário preencheu nome e email porém a senha é menor que 8
  if Usuario.objects.filter(email=email).exists():
    messages.add_message(request,constants.WARNING,'Usuário já cadastrado')
    return redirect("/auth/register/")
    #Se o usuario já é cadastrado
  if Usuario.objects.filter(username=nome).exists():
    messages.add_message(request,constants.WARNING,'Já existe um usuário com esse nome no sistema')
    return redirect("/auth/register/")
  
  # Caso não tenha erro, cadastrar no banco de dados
  try:
    usuario = Usuario.objects.create_user(username=nome,email=email,password=senha, setor=setor,matricula=matricula)
    usuario.save()
    messages.add_message(request,constants.SUCCESS,"Usuário cadastrado com sucesso.")
    return redirect("/auth/register/")
    # Deu tudo ta certo
  except:
    messages.add_message(request,constants.ERROR,"Erro interno do servidor")
    return redirect("/auth/register/")
    # Erro interno do sistema

def validar_login(request):
  nome = request.POST.get('nome')
  senha = request.POST.get('senha')
  usuario = auth.authenticate(request,username = nome, password = senha)
  if not usuario:
    messages.add_message(request,constants.ERROR,"Usuário ou senha incorretos")
    return redirect("/auth/login/")
  else:
    auth.login(request,usuario)
    return redirect("/auth/usuarios/")

def logout(request):
  auth.logout(request)
  return redirect("/auth/login/")
  
def login(request):
  if request.user.is_authenticated:
    return redirect('/auth/usuarios')
  return render(request,"login.html")

def register(request):
  status = request.GET.get('status')
  return render(request,"register.html",{"status":status})


@login_required(login_url="/auth/login/")
def index(request):
  usuarios = Usuario.objects.all()
  return render(request,"lista_usuarios.html",{"usuarios":usuarios})