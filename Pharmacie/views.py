
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from Pharmacie.forms import LoginForm, SearchForm
from Pharmacie.services.savepharma_service import SavePharmaService
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages

# Create your views here.

def home(request):

    listCommune=Commune.objects.all()
    form=SearchForm()
    context={
        'commune':listCommune,
        'form':form
    }
    return render(request, "pages/index.html", context)

def getPharmaCom(request):
    form=SearchForm()
    if request.method=='GET':
        form=SearchForm(request.GET)
        if form.is_valid():
            adr=form.cleaned_data['address']
            ph=Pharmacie.objects.filter(com__com_lib=adr)
            first=Pharmacie.objects.filter(com__com_lib=adr)[0]
            
            context={
                'pharmacie':ph,
                'first':first,
            }
            return render(request, "pages/pharmacie.html", context)
    return render(request, "pages/pharmacie.html")

def login(request):
    form=LoginForm()
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            try:
                name=User.objects.get(email=username)
                user = authenticate(username=name, password=password)
                auth_login(request, user)
                messages.success(request, f"Vous êtes connecté(e)s avec succès {user.username.upper()} !!!")
                return redirect("/admin")
            except:
                messages.error(request, "Email ou mot de passe invalide")
                redirect('/admin')
        else:
            messages.error(request, "Email ou mot de passe invalide")
                     
    context={"form":form}
    return render(request, "admin/login.html", context)

def saveData(request):
    garde=Garde.objects.latest('gar_id')
    # garde=garde.reverse()[:1]
    Pharmacie.objects.all().delete()
    savePh=SavePharmaService(garde)
    save=savePh.save_pharmacie()
    if save==True:
        return HttpResponse('save avec success')
    
    return HttpResponse('no save')
    

