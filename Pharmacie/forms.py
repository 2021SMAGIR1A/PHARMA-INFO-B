from django import forms
from django.forms import ModelChoiceField

from Pharmacie.models import Commune

class ComModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return " %s " % obj.com_lib

class SearchForm(forms.Form):
    address = ComModelChoiceField(queryset=Commune.objects.all(), widget =forms.Select(attrs={'class': 'form-control', 'id':"select2", 'style':"width: 84%; height:150%"}), label='')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg','id':"form2Example17", 'placeholder': 'Entrez votre email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':"form2Example27",'class':"form-control form-control-lg",'placeholder': 'Entrer votre mot de passe'}))

# class SearchForm(forms.Form):
#     address=ComModelChoiceField(error_messages={'required':''},queryset=Commune.objects.all(),
#                            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': '-- Selectionnez une zone --', 'required':True, 'id':"select2", 'style':"width: 84%; height:150%"}), 
#                            label='')
#     def clean(self):
#         cleaned_data=super(SearchForm, self).clean()
        
#         search=cleaned_data.get('search')
        
#         return cleaned_data
            
    