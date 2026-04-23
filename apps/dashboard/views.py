from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render
from apps.patients.models import Patient
from apps.results.models import Result
from apps.tests.models import TestRequest


@login_required
def dashboard_home(request):
    today = timezone.localdate()
    context = {
        'total_patients': Patient.objects.count(),
        'total_requests': TestRequest.objects.count(),
        'pending_tests': TestRequest.objects.filter(status='pending').count(),
        'completed_tests': TestRequest.objects.filter(status='completed').count(),
        'today_registrations': Patient.objects.filter(created_at__date=today).count(),
        'today_results': Result.objects.filter(entered_at__date=today).count(),
        'recent_requests': TestRequest.objects.select_related('patient', 'test_type', 'assigned_to')[:8],
        'test_breakdown': TestRequest.objects.values('test_type__name').annotate(total=Count('id')).order_by('-total')[:5],
    }
    return render(request, 'dashboard/home.html', context)
