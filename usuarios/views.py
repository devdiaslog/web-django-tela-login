from django.shortcuts import render
from django.shortcuts import redirect
from .models import Usuarios
from hashlib import sha256
from django.contrib import messages
from django.contrib.messages import constants
from django.http.response import HttpResponse


def validar_register(request):
  nome = request.POST.get('nome')
  email = request.POST.get('email')
  senha = request.POST.get('senha')
  
  if len(nome.strip()) == 0 or len(email.strip()) == 0:
    messages.add_message(request,constants.ERROR,"Nome e e-mail devem ser preenchidos.")
    return redirect("/auth/register/")
    # Se o usuário não digitou nada
  if len(senha)<8:
    messages.add_message(request,constants.INFO,"A senha deve conter pelo 8 dígitos")
    return redirect("/auth/register/")
    # Se o usuário preencheu nome e email porém a senha é menor que 8
  usuario = Usuarios.objects.filter(email=email)
  if len(usuario) > 0:
    messages.add_message(request,constants.WARNING,'Usuário já cadastrado')
    return redirect("/auth/register/")
    #Se o usuario já é cadastrado
  
  # Caso não tenha erro, cadastrar no banco de dados
  try:
    senha = sha256(senha.encode()).hexdigest()
    usuario = Usuarios(nome=nome,email=email,senha=senha)
    usuario.save()
    messages.add_message(request,constants.SUCCESS,"Usuário cadastrado com sucesso.")
    return redirect("/auth/register/")
    # Deu tudo ta certo
  except:
    messages.add_message(request,constants.ERROR,"Erro interno do servidor")
    return redirect("/auth/register/")
    # Erro interno do sistema

def validar_login(request):
  email = request.POST.get('email')
  senha = request.POST.get('senha')
  senha = sha256(senha.encode()).hexdigest()
  usuario = Usuarios.objects.filter(email=email).filter(senha=senha)
  if len(usuario) > 0:
    request.session['usuario_logado'] = True
    return redirect("/auth/usuarios/")
  else:
    messages.add_message(request,constants.ERROR,"Usuário ou senha incorretos")
    return redirect("/auth/login/")
    #Usuario ou senha incorreto

def logout(request):
  request.session.flush()
  return redirect("/auth/login/")
  
def login(request):
  status = request.GET.get("status")
  return render(request,"login.html",{"status":status})

def register(request):
  status = request.GET.get('status')
  return render(request,"register.html",{"status":status})

def index(request):
  if request.session.get('usuario_logado'):
    usuarios = Usuarios.objects.all()
    return render(request,"lista_usuarios.html",{"usuarios":usuarios})
  messages.add_message(request,constants.WARNING,"Faça login para continuar.")
  return redirect("/auth/login/")