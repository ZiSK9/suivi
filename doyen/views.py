from django.shortcuts import render,redirect
from pages.models import inscription,reinscription,edition_pv,Doctorant,situation_doctorant
from .models import login_doyen
from django.contrib import messages
from encadreur.models import Encadreur

# Create your views here.
def doyen_login(request):
    return render(request,'doyen/login.html')
def dashboards(request):
    return render(request,'doyen/dashboards.html')

def index_doyen(request) :
    if request.method == 'POST':
        username = request.POST.get('username_doyen')
        password = request.POST.get('password_doyen')
        try:
            user=login_doyen.objects.get(username=username)
            if user.authenticate(username, password):
                # Authentication successful, redirect to the "demande_etat_avancement" page
                return redirect('dashboards')
            else:
                # Authentication failed, set an error message
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        except login_doyen.DoesNotExist:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        except login_doyen.MultipleObjectsReturned:
            messages.error(request, "Plusieurs comptes avec ce nom d'utilisateur existent. Veuillez contacter l'administration.")

    return render(request, 'doyen/login.html')
    

def liste_inscription_doyen(request):
    inscriptions = inscription.objects.all()
    return render(request, 'doyen/inscription.html', {'inscriptions': inscriptions})

def liste_reinscription_doyen(request):
    reinscriptions = reinscription.objects.all()
    return render(request, 'doyen/reinscription.html', {'reinscriptions': reinscriptions})


def editionPVdoyen(request):
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'edition').all()
    editions=edition_pv.objects.all()
    return render(request, 'doyen/editionPVDoyen.html', {'doctorants': doctorants, 'editions': editions})
    


def etat_Avencement_doyen(request) :
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'situation_doctorant').all()
    situations = situation_doctorant.objects.all()
    return render(request,'doyen/etat_d`avencement.html', {'doctorants': doctorants,'situations': situations})


def soutenances(request):
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'soutenance').all()
    encadreurs = Encadreur.objects.all()
    return render(request, 'doyen/soutenancesDoyen.html', {'doctorants': doctorants, 'encadreurs': encadreurs})


#affiche les instance des inscription



    


