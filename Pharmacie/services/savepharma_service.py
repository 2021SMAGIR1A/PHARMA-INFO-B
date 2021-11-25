from Pharmacie.models import Commune, Pharmacie
from Pharmacie.services.pharmacie_service import PharmacieService

class SavePharmaService():

    bool=False
    def __init__(self, garde):
        self.garde=garde

    def save_pharmacie(self):
        d=None
        ph=PharmacieService()
        data=ph.getDataPharmacie()
        for k in data:
            d=Commune.objects.get(com_lib=k)
            if d is None:
                d=Commune.objects.create(com_lib=k)
            for i, tb in data[k].items():
                for t in tb:
                    self.sph(d, t)
                    self.bool=True
        return self.bool

    def sph(self, d, tb):
        Pharmacie.objects.create(
                    com=d,
                    gar=self.garde,
                    ph_adresse=tb['adresse'],
                    ph_nom=tb['name'],
                    ph_lat=tb['position'][0] if tb['position'] != "" else 0,
                    ph_lng=tb['position'][1] if tb['position'] != "" else 0
                )
