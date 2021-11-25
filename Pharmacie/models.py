# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Commune(models.Model):
    com_id = models.AutoField(primary_key=True)
    com_lib = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commune'
    
    def __str__(self):
        return self.com_lib


class Garde(models.Model):
    gar_id = models.AutoField(primary_key=True)
    gar_dated = models.DateField(db_column='gar_dateD', blank=True, null=True)  # Field name made lowercase.
    gar_datef = models.DateField(db_column='gar_dateF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'garde'

    def __str__(self):
        return '{0} - {1}'.format(self.gar_dated, self.gar_datef)

class Pharmacie(models.Model):
    ph_id = models.AutoField(primary_key=True)
    com = models.ForeignKey(Commune, models.DO_NOTHING)
    gar = models.ForeignKey(Garde, models.DO_NOTHING)
    ph_lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    ph_lng = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    ph_adresse = models.CharField(max_length=70, blank=True, null=True)
    ph_nom = models.CharField(max_length=70, blank=True, null=True)
    ph_user_traite=models.ManyToManyField(User, through="Traiter")

    class Meta:
        managed = False
        db_table = 'pharmacie'

    def __str__(self):
        return self.ph_nom

class Traiter(models.Model):
    id_tr = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user')
    ph = models.ForeignKey(Pharmacie, models.DO_NOTHING)
    datecreate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traiter'
        unique_together = (('user', 'ph'),)
    
    def __str__(self):
        return self.user+' - '+self.ph

