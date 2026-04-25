from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Patient
from .forms import PatientForm


def patient_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(patient_number__icontains=query)
        )

    return render(request, 'patients/list.html', {
        'patients': patients,
        'query': query
    })


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient added successfully.")
            return redirect('patients:list')
    else:
        form = PatientForm()

    return render(request, 'patients/form.html', {'form': form})


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/detail.html', {'patient': patient})


def patient_update(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit patients.")

    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient updated successfully.")
            return redirect('patients:list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/form.html', {'form': form})


def patient_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete patients.")

    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        patient.delete()
        messages.success(request, "Patient deleted successfully.")
        return redirect('patients:list')

    return render(request, 'patients/confirm_delete.html', {'patient': patient})