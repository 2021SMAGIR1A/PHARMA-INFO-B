from django.contrib import admin

from Pharmacie.models import Commune, Garde, Pharmacie, Traiter

# Register your models here.
# from django.contrib.admin import AdminSite

# class MyAdminSite(AdminSite):
#     login_template = 'admin/login.html'

# site = MyAdminSite()
admin.site.register(Commune)
admin.site.register(Pharmacie)
admin.site.register(Traiter)
admin.site.register(Garde)





