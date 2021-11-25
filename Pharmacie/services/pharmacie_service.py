
import requests
from bs4 import BeautifulSoup
import folium
from django.shortcuts import render
import geocoder
from geopy import distance
import json


class PharmacieService:

    secteur = []
    title = []
    data={}

    def getDataPharmacie(self):
        url = "https://pharma-consults.net/pharmacies-gardes"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('div',  {'class': 'table-responsive'})
        titles = table.find_all('h5',  {'class': 'kt-portlet__head-title'})
        rows = table.find_all('table')
        td=[]
        
        for tle in titles:
            self.title.append(tle.text.strip())

        for rx in rows:
            tr = rx.find('tbody').find_all('tr')
            td.append([x.find_all('td') for x in tr])
        
        dt=[]
        for line in td:
            for d in line:
                dt.append({'name':d[0].text, 'adresse':d[3].text, 'position':self.getLatLon(d[4].a.get('href')) if d[4].a is not None else "", 'datD':d[5].text, 'datF':d[6].text})
                
            self.secteur.append(dt)
            dt=[]

        for idx, tle in enumerate(self.title):
            self.data[tle]={'table': self.secteur[idx]}

        result=json.dumps(self.data)
        result=json.loads(result)
        return result
    
    def getLatLon(self, str):
        tab=str.split('@')
        del tab[0]
        data1=" ".join(tab)
        first=data1.split('/')
        splitPos=first[0]
        pos=splitPos.split(',')
        if len(pos)==3:
            del pos[2]
        return (float(pos[0]), float(pos[1]))

    def getPharmacie(self, num):
        result=json.dumps(self.data[num])
        result=json.loads(result)
        return result
