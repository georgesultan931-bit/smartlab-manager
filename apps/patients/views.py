from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from apps.common import create_audit_log
from .forms import PatientForm
from .models import Patient


@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(Q(full_name__icontains=query) | Q(patient_number__icontains=query) | Q(phone__icontains=query))
    paginator = Paginator(patients, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'patients/patient_list.html', {'page_obj': page_obj, 'query': query})


@login_required
def patient_create(request):
    form = PatientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        patient = form.save()
        create_audit_log(user=request.user, action='create', instance=patient, description=f'Created patient {patient.full_name}')
        messages.success(request, 'Patient registered successfully.')
        return redirect('patients:list')
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Register Patient'})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if request.method == 'POST' and form.is_valid():
        patient = form.save()
        create_audit_log(user=request.user, action='update', instance=patient, description=f'Updated patient {patient.full_name}')
        messages.success(request, 'Patient updated successfully.')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Edit Patient'})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_detail.html', {'patient': patient})
