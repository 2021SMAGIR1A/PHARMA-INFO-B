
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from Pharmacie.forms import LoginForm, SearchForm
from Pharmacie.services.savepharma_service import SavePharmaService
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from openrouteservice import client

import folium
import geocoder
from geopy import distance
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
            request.session['addr']=first.com.com_lib
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
    
def mapjs(request):
    if request.method == 'GET':
        lat=request.GET.get('lat')
        lng=request.GET.get('lng')
        request.session['lat']=lat
        request.session['lng']=lng
    return HttpResponse(200)


def getMapPharma(request):

    # api_key = '5b3ce3597851110001cf624893d04f8dbfd444dfa5e4377454592c0f' #https://openrouteservice.org/sign-up
    # clnt = client.Client(key=api_key)


    lat=float(request.session['lat'])
    lng=float(request.session['lng'])
    adr=request.session['addr']
    secteur=Pharmacie.objects.filter(com__com_lib=adr)
    thisCoord=[lat, lng]
    m = folium.Map(location=thisCoord, zoom_start=13)
    getListDistance={}

    for ville in secteur:
        position=getAdress(ville.ph_nom, ville.com.com_lib)
        if position.status == 'OK':
            distancePos=distance.distance(thisCoord, position.latlng)
            getListDistance[ville.ph_nom]= distancePos
        else:
            name=ville.ph_nom
            name=name.replace('PHCIE','PHARMACIE')
            if '(' in name:
                name=name.split('(')
                name=name[0][:-1]
            distancePos=distance.distance(thisCoord, (ville.ph_lat, ville.ph_lng))
            getListDistance[ville.ph_nom]= distancePos

    numPharma=min(getListDistance, key=getListDistance.get)
    latLng2=getAdress(numPharma, adr)
    if latLng2.latlng is None:
        l=Pharmacie.objects.filter(ph_nom=numPharma)
        for x in l:
            latLng2={
                "lat":x.ph_lat,
                "lng":x.ph_lng,
                "address":x.ph_adresse
            }

    coordinates=None
    for ville in secteur:
        if numPharma == ville.ph_nom:
            if type(latLng2) == dict:
                coordinates = [thisCoord, [latLng2['lat'], latLng2['lng']]]
                folium.Marker(coordinates[1], icon=folium.Icon(color='green'), popup=f'<b>{ latLng2["address"] }</b><br>{ (latLng2["lat"], latLng2["lng"]) }', tooltip=latLng2["address"]).add_to(m)
            else:
                coordinates = [thisCoord, latLng2.latlng]
                folium.Marker(coordinates[1], icon=folium.Icon(color='green'), popup=f'<b>{ latLng2.address }</b><br>{ latLng2.latlng }', tooltip=latLng2.address).add_to(m)
        else:
            position=getAdress(ville.ph_nom, ville.com.com_lib)
            if position.status == 'OK':
                folium.Marker(position.latlng, popup=f'<b>{ position.address }</b><br>{ position.latlng }', tooltip=position.address).add_to(m)
            else:
                folium.Marker((ville.ph_lat, ville.ph_lng), popup=f'<b>{ ville.ph_nom }</b><br>{ (ville.ph_lat, ville.ph_lng) }', tooltip=ville.ph_nom).add_to(m)



    
   
    # popup_route = "<h4>{0} route</h4><hr>" \
    #              "<strong>Duration: </strong>{1:.1f} mins<br>" \
    #              "<strong>Distance: </strong>{2:.3f} km"

    # # Request route 5.319141053051958, -4.099392858622073
    # direction_params = {'coordinates': coordinates,
    #                     'profile': 'driving-car',
    #                     'format_out': 'geojson',
    #                     'preference': 'shortest',
    #                     'geometry': 'true'}

    # regular_route = clnt.directions(**direction_params) # Direction request

    # # Build popup
    # distances, duration = regular_route['features'][0]['properties']['summary'].values()
    # popup = folium.map.Popup(popup_route.format('Regular',
    #                                                  duration/60,
    #                                                  distances/1000))

    # gj= folium.GeoJson(regular_route,
    #                    name='Regular Route',
    #                    style_function=style_function('blue')) \
    #           .add_child(popup)\
    #           .add_to(m)

    folium.Marker(coordinates[0],icon=folium.Icon(color='red'),
     popup=f'<b>Your location</b><br>Latitude: {thisCoord[0]} <br>Longitude: {thisCoord[1]} ', tooltip="Me").add_to(m)

    # folium.PolyLine([[latLng2['lat'], latLng2['lng']],thisCoord],tooltip = "itinéraire Rennes-Grenoble").add_to(m)




    context={
        'm':m._repr_html_(),
    }
    return render(request, 'pages/map.html', context)


def style_function(color): # To style data
    return lambda feature: dict(color=color,
                                opacity=0.5,
                                weight=4,)


def getAdress(name, title):
    name=name.replace('PHCIE','PHARMACIE')
    if '(' in title:
        title=title.split('(')
        title=title[0][:-1]
    if '/' in title:
        title=title.split('/')
        title=title[0]
    if '(' in name:
        name=name.split('(')
        name=name[0][:-1]
    # print(title)
    address = '{0}, {1}, côte d\'ivoire'.format(name, title)
    location = geocoder.osm(address)
    return location
