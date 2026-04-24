from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Patient
from .forms import PatientForm


# LIST + SEARCH
def patient_list(request):
    query = request.GET.get('q', '')

    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(request, 'patients/list.html', {
        'patients': patients,
        'query': query
    })


# CREATE
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients:list')
    else:
        form = PatientForm()

    return render(request, 'patients/form.html', {'form': form})


# DETAIL
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/detail.html', {'patient': patient})


# UPDATE
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patients:list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/form.html', {'form': form})