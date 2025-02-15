from django.shortcuts import render, redirect
from main import fetch_emploi_du_temps
from django.http import JsonResponse
from django.http import HttpResponseRedirect

def execute_main_script(request):
    if request.method == "GET":
        result = {"message": "Le script principal a été exécuté avec succès."}
        return JsonResponse(result)
    else:
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)


def login_and_fetch_schedule(request):
    emploi_du_temps = request.session.get('emploi_du_temps')

    if emploi_du_temps:
        return render(request, 'result.html', {'emploi_du_temps': emploi_du_temps})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        emploi_du_temps = fetch_emploi_du_temps(username, password)

        if emploi_du_temps:
            request.session['emploi_du_temps'] = emploi_du_temps
            return render(request, 'result.html', {'emploi_du_temps': emploi_du_temps})
        else:
            return HttpResponseRedirect('/app/fetch-schedule/?error=motdepasseincorrect')

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()  # Cela efface toutes les données de la session
    return redirect('/app/fetch-schedule/')

#JaiUnNouveauPcEn2018_