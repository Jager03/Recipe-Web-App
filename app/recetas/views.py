# recetas/views.py
from django.shortcuts import render, redirect
from django.shortcuts import  HttpResponse
from .models import FotoReceta, Receta, Ingrediente
from django.utils import timezone
from django.template import Template, Context
from pathlib import Path
from mi_sitio import settings
from .forms import RecetaForm, IngredienteForm
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.

def index(request):
    recetas = Receta.objects.all()
    modalFlag = False
    
    if 'modeFlag' in request.COOKIES:
        if 'modal' in request.GET:
            modalFlag = True
            return render(request, 'home.html', {'flag': request.COOKIES['modeFlag'], 'recetas': recetas, 'media_url':settings.MEDIA_URL, 'modalFlag': modalFlag})
        else:
            return render(request, 'home.html', {'flag': request.COOKIES['modeFlag'], 'recetas': recetas, 'media_url':settings.MEDIA_URL, 'modalFlag': modalFlag})
    else:
        return render(request, 'home.html', {'flag': False, 'recetas': recetas, 'media_url':settings.MEDIA_URL})


    

def detalles(request, nombre_id):
    receta = Receta.objects.get(nombre=nombre_id)
    ingredientes= Ingrediente.objects.filter(receta = receta) 
    

    context = {
        'receta':receta, 
        'media_url':settings.MEDIA_URL,
        'ingredientes': ingredientes
    }
    return render(request, 'detalles.html', context ) 


def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        receta = Receta.objects.get(nombre__contains=search)

        
        return render(request, 'searchbar.html', { 'receta':receta, 'media_url':settings.MEDIA_URL} ) 


#Problema: Esta funcion devuelve siempre cookie False! Por que?
def toggleMode(request):
    if 'modeFlag' in request.COOKIES:
        flag =  request.COOKIES['modeFlag']
    else:
         flag = False


    if 'modeFlag' in request.COOKIES:
        flag = not flag
        response = render(request, 'home.html', {'flag': flag})
        response.set_cookie('modeFlag', flag)
        return response
    else:
        return render(request, 'home.html', {'flag': flag})


def deleteView(request, nombre_id):
    if request.user.is_superuser:
        Receta.objects.get(nombre=nombre_id).delete()
        messages.success(request, ("Se ha borrado la receta"))
    else:
        messages.success(request, ("No puedes borrar receta: No eres super usuario"))
        
    return  HttpResponseRedirect('/')
        

def updateView(request, nombre_id):
    receta = Receta.objects.get(nombre=nombre_id)
    form = RecetaForm(request.POST or None, instance=receta) #si van a postear: usar este form, sino None 
    if request.user.is_staff:
        if form.is_valid():
            form.save()
            messages.success(request, ("Receta actualizada"))
            return redirect('/')
    else:
        messages.success(request, ("No puedes actualizar receta: No eres usuario staff"))
        return redirect('/')

    context={
        'receta': receta,
        'form': form
    }

    return render(request, 'update.html', context )


def add(request):
    if request.user.is_superuser:
        enviado = False
        if request.method == "POST":
            form = RecetaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Se ha añadido correctamente la receta"))
                return HttpResponseRedirect('/add?enviado=True') #redireccionar a pagina add pero esta vez con true en enviado
        else:
            form = RecetaForm
            if 'enviado' in request.GET:
                enviado = True
    else:
        messages.success(request, ("No puedes añadir receta: No eres super usuario"))
        return redirect('/')
    
    context = {
        'form': form,
        'enviado': enviado
    }

    return render(request, 'add.html', context )


def addIng(request):
    if request.user.is_superuser:
        enviado = False
        if request.method == "POST":
            form = IngredienteForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/addIng?enviado=True') #redireccionar a pagina add pero esta vez con true en enviado
        else:
            form = IngredienteForm
            if 'enviado' in request.GET:
                enviado = True
    else:
        messages.success(request, ("No puedes añadir ingrediente: No eres super usuario"))
        return redirect('/')
    
    context = {
        'form': form,
        'enviado': enviado
    }

    return render(request, 'addIng.html', context )