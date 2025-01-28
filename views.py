from django.shortcuts import render, get_object_or_404, redirect
from .models import TutorCoordinatori, TutorCollaboratori

def edit_tutor(request, id):
    tutor = get_object_or_404(TutorCoordinatori, id=id)
    if request.method == 'POST':
        tutor.nome = request.POST.get('nome')
        tutor.cognome = request.POST.get('cognome')
        tutor.email = request.POST.get('email')
        tutor.telefono = request.POST.get('telefono')
        tutor.dipartimento = request.POST.get('dipartimento')
        tutor.save()
        return redirect('tutor_coordinatori')
    return render(request, 'edit_tutor.html', {'tutor': tutor})

def edit_tutor_collaboratore(request, id):
    tutor = get_object_or_404(TutorCollaboratori, id=id)
    if request.method == 'POST':
        tutor.nome = request.POST.get('nome')
        tutor.cognome = request.POST.get('cognome')
        tutor.email = request.POST.get('email')
        tutor.telefono = request.POST.get('telefono')
        tutor.dipartimento = request.POST.get('dipartimento')
        tutor.save()
        return redirect('tutor_collaboratori')
    return render(request, 'edit_tutor_collaboratore.html', {'tutor': tutor})
