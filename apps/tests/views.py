from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from apps.common import create_audit_log
from .forms import TestRequestForm, TestTypeForm
from .models import TestRequest, TestType


@login_required
def test_request_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    test_requests = TestRequest.objects.select_related('patient', 'test_type', 'assigned_to').all()
    if query:
        test_requests = test_requests.filter(Q(patient__full_name__icontains=query) | Q(patient__patient_number__icontains=query) | Q(test_type__name__icontains=query))
    if status:
        test_requests = test_requests.filter(status=status)
    paginator = Paginator(test_requests, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'tests/test_request_list.html', {'page_obj': page_obj, 'query': query, 'status': status})


@login_required
def test_request_create(request):
    form = TestRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        test_request = form.save(commit=False)
        test_request.requested_by = request.user
        test_request.save()
        create_audit_log(user=request.user, action='create', instance=test_request, description=f'Created test request for {test_request.patient.full_name}')
        messages.success(request, 'Test request created successfully.')
        return redirect('tests:list')
    return render(request, 'tests/test_request_form.html', {'form': form, 'title': 'Create Test Request'})


@login_required
def test_request_update(request, pk):
    test_request = get_object_or_404(TestRequest, pk=pk)
    form = TestRequestForm(request.POST or None, instance=test_request)
    if request.method == 'POST' and form.is_valid():
        test_request = form.save()
        create_audit_log(user=request.user, action='update', instance=test_request, description=f'Updated test request #{test_request.pk}')
        messages.success(request, 'Test request updated successfully.')
        return redirect('tests:list')
    return render(request, 'tests/test_request_form.html', {'form': form, 'title': 'Edit Test Request'})


@login_required
def test_type_list(request):
    test_types = TestType.objects.all()
    return render(request, 'tests/test_type_list.html', {'test_types': test_types})


@login_required
def test_type_create(request):
    form = TestTypeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        test_type = form.save()
        create_audit_log(user=request.user, action='create', instance=test_type, description=f'Created test type {test_type.name}')
        messages.success(request, 'Test type created successfully.')
        return redirect('tests:type_list')
    return render(request, 'tests/test_type_form.html', {'form': form, 'title': 'Create Test Type'})
