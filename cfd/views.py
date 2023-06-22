from django.shortcuts import render,redirect
from .models import login_cfd,ApplicationSettings
from django.contrib.auth import authenticate
from django.contrib import messages
from pages.models import reinscription,inscription
from pages.models import situation_doctorant
from pages.models import edition_pv,Doctorant,Soutenance,Passage
from django.core.exceptions import ObjectDoesNotExist
from encadreur.models import Encadreur



# Create your views here.

def login_CFD(request) :
    return render(request,'admins/index.html')
def dashboard(request) :
    return render(request,'admins/dashboard.html')


def indexCFD(request):
    if request.method == 'POST':
        username = request.POST.get('username_cfd')
        password = request.POST.get('password_cfd')
        try:
            user=login_cfd.objects.get(username=username)
            if user.authenticate(username, password):
                # Authentication successful, redirect to the "demande_etat_avancement" page
                return redirect('dashboard')
            else:
                # Authentication failed, set an error message
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        except login_cfd.DoesNotExist:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        except login_cfd.MultipleObjectsReturned:
            messages.error(request, "Plusieurs comptes avec ce nom d'utilisateur existent. Veuillez contacter l'administration.")

    return render(request, 'admins/index.html')

def liste_inscription(request) :
    inscriptions = inscription.objects.all()
    return render(request, 'admins/inscription.html', {'inscriptions': inscriptions})

def liste_reinscription(request) :
    reinscriptions = reinscription.objects.all()
    return render(request, 'admins/reinscription.html', {'reinscriptions': reinscriptions})

def control_reinscription(request):
    application_settings = ApplicationSettings.objects.first()
    if application_settings:
        if application_settings.reinscription_open:
            current_status = 'Etat : Inscription et Réinscription est ouverte.'
        else:
            current_status = 'Etat : Inscription et Réinscription est fermée.'
        messages.info(request, current_status)
    if request.method == 'POST':
        reinscription_status = request.POST.get('control')
        
        # Update the ApplicationSettings model based on the selected option
        application_settings = ApplicationSettings.objects.first()
        if application_settings:
            application_settings.reinscription_open = reinscription_status == 'open'
            application_settings.save()
            
            if application_settings.reinscription_open:
                message = 'Inscription et Réinscription est ouverte.'
            else:
                message = 'Inscription et Réinscription est fermée.'
                
            messages.success(request, message)
        
    return render(request, 'admins/control_reinscription.html')
    

def edition_PV_view(request) :
    return render(request, 'admins/editionpv.html')

def edition_PV(request):
    entries = edition_pv.objects.all()

    if request.method == 'POST':
        numero_inscription = request.POST.get('numero_inscription')
        nom_prenom = request.POST.get('nom_prenom')
        cours_de_specialite = request.POST.get('cours_de_specialite')
        methodologie = request.POST.get('methodologie')
        competences_anglais = request.POST.get('competences_anglais')
        communications = request.POST.get('communications')
        communications2 = request.POST.get('communications2')
        publications = request.POST.get('publications')
        tic = request.POST.get('tic')

        try:
            pv_entry = edition_pv.objects.get(numero_inscription=numero_inscription)
            pv_entry.nom_prenom = nom_prenom
            
            if int(cours_de_specialite) > 12:
                # If cours_de_specialite exceeds 12, display an error message
                messages.error(request, 'Cours de spécialité should not exceed 12.')
            else:
                pv_entry.cours_de_spécialité = cours_de_specialite
            
            if int(methodologie) > 6:
                # If methodologie exceeds 6, display an error message
                messages.error(request, 'Méthodologie should not exceed 6.')
            else:
                pv_entry.methodologie = methodologie
            
            if int(competences_anglais) > 6:
                # If compétences_anglais exceeds 6, display an error message
                messages.error(request, 'Compétences en anglais should not exceed 6.')
            else:
                pv_entry.compétences_anglais = competences_anglais
            
            pv_entry.communications = communications
            pv_entry.communications2 = communications2

            pv_entry.publications = publications
            pv_entry.tic = tic
        except ObjectDoesNotExist:
            if int(cours_de_specialite) > 12:
                # If cours_de_specialite exceeds 12, display an error message
                messages.error(request, 'Cours de spécialité should not exceed 12.')
                return redirect('editionPV')  # Redirect back to the form page
            
            if int(methodologie) > 6:
                # If methodologie exceeds 6, display an error message
                messages.error(request, 'Méthodologie should not exceed 6.')
                return redirect('editionPV')  # Redirect back to the form page
            
            if int(competences_anglais) > 6:
                # If compétences_anglais exceeds 6, display an error message
                messages.error(request, 'Compétences en anglais should not exceed 6.')
                return redirect('editionPV')  # Redirect back to the form page
            
            pv_entry = edition_pv.objects.create(
                numero_inscription=numero_inscription,
                nom_prenom=nom_prenom,
                cours_de_spécialité=cours_de_specialite,
                methodologie=methodologie,
                compétences_anglais=competences_anglais,
                communications=communications,
                communications2=communications2,
                publications=publications,
                tic=tic
            )

        pv_entry.calculate_total()
        pv_entry.save()

        return redirect('editionPV')  # Replace 'success_url' with the URL or name of your success page

    context = {
        'entries': entries
    }
    return render(request, 'admins/editionpv.html', context)




def demandes_comptes(request):
    if request.method == 'POST':
        doctorant_id = request.POST.get('doctorant_id')
        action = request.POST.get('action')
        encadreur_id = request.POST.get('encadreur_id')
        action_encadreur = request.POST.get('action_encadreur')
        
        if doctorant_id:
            doctorant = Doctorant.objects.get(id=doctorant_id)
            
            if action == 'accept':
                doctorant.validation = True
                doctorant.save()
            elif action == 'reject':
                doctorant.validation = False
                doctorant.save()

        if encadreur_id:
            encadreur = Encadreur.objects.get(id=encadreur_id)
            
            if action_encadreur == 'accept':
                encadreur.validation = True
                encadreur.save()
            elif action_encadreur == 'reject':
                encadreur.validation = False
                encadreur.save()

        return redirect('demandesComptes')  # Redirect back to the same page after processing the request

    doctorants = Doctorant.objects.all()
    encadreurs = Encadreur.objects.all()
    return render(request, 'admins/demandes_comptes.html', {'doctorants': doctorants, 'encadreurs': encadreurs})


def etat_Avencement(request) :
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'situation_doctorant').all()
    situations = situation_doctorant.objects.all()
    return render(request,'admins/etat_d`avencement.html', {'doctorants': doctorants,'situations': situations})

def ajouterEncadreur(request):
    if request.method == 'POST':
        doctorant_id = request.POST.get('doctorant')
        encadreur_id = request.POST.get('encadreur')

        doctorant = Doctorant.objects.get(id=doctorant_id)
        encadreur = Encadreur.objects.get(id=encadreur_id)

        doctorant.encadreur = encadreur
        doctorant.save()
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription').all()
    encadreurs = Encadreur.objects.all()
    return render(request, 'admins/encadreurs.html', {'doctorants': doctorants, 'encadreurs': encadreurs})




def edition_PV_2(request):
    if request.method == 'POST':
        selected_users = request.POST.getlist('doctorant')  # Get a list of selected user IDs
        for user_id in selected_users:
            doctorant = Doctorant.objects.get(id=user_id)

            cours_de_specialite = request.POST.get('cours_de_specialite')
            methodologie = request.POST.get('methodologie')
            competences_anglais = request.POST.get('competences_anglais')
            communications1 = request.POST.get('communications1')
            communications2 = request.POST.get('communications2')
            publication1 = request.POST.get('publication1')
            publication2 = request.POST.get('publication2')
            publication3 = request.POST.get('publication3')
            publication4 = request.POST.get('publication4')
            publication5 = request.POST.get('publication5')
            tic = request.POST.get('Tic')
            brevet = request.POST.get('brevet')
            try:
                pv_entry = edition_pv.objects.get(doctorant=doctorant)
            except edition_pv.DoesNotExist:
                pv_entry = edition_pv(doctorant=doctorant)

            pv_entry.cours_de_spécialité = cours_de_specialite
            pv_entry.methodologie = methodologie
            pv_entry.compétences_anglais = competences_anglais
            pv_entry.communications1 = communications1
            pv_entry.communications2 = communications2
            pv_entry.publication1 = publication1
            pv_entry.publication2 = publication2
            pv_entry.publication3 = publication3
            pv_entry.publication4 = publication4
            pv_entry.publication5 = publication5
            pv_entry.tic = tic
            pv_entry.brevet = brevet
            pv_entry.calculate_total()
            pv_entry.save()

    
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'edition').all()
    editions=edition_pv.objects.all()
    return render(request, 'admins/edition_pv.html', {'doctorants': doctorants, 'editions': editions})

def demandes_soutenances(request):
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'soutenance').all()
    encadreurs = Encadreur.objects.all()
    if request.method == 'POST':
        doctorant_id = request.POST.get('doctorant')
        action = request.POST.get('action')
        csd_csf = request.FILES.get('csd_csf')
        autorisation_soutenance = request.FILES.get('autorisation_soutenance')
        pv_soutenance = request.FILES.get('pv_soutenance')
        doctorant = Doctorant.objects.get(id=doctorant_id)
        
        # Update the value of action based on the received action value
        if action == 'accept':
            action_value = True
        else:
            action_value = False
        
        new_demande = Soutenance(
            doctorant=doctorant,
            csd_csf=csd_csf,
            autorisation_soutenance=autorisation_soutenance,
            pv_soutenance=pv_soutenance,
            action=action_value  # Use the updated action value
        )
        new_demande.save()
    return render(request, 'admins/demandes_soutenances.html', {'doctorants': doctorants, 'encadreurs': encadreurs})


def passages_annees(request):
    if request.method == 'POST':
        doctorant_id = request.POST.get('doctorant_id', None)
        action = request.POST.get('action', None)
        if doctorant_id is not None:
            doctorant = Doctorant.objects.get(id=doctorant_id)
            passage=Passage.objects.get(doctorant=doctorant)
            if action == 'accept':
                passage.passage_annee_validation = True
            elif action == 'reject':
                passage.passage_annee_validation = False
            passage.save()
        return redirect('demandesPassage')

    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription','passage').all()
    return render(request, 'admins/passages_annees.html', {'doctorants': doctorants})





    