from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from .models import AuditLog


@login_required
def audit_log_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access denied")

    logs = AuditLog.objects.select_related('user').order_by('-created_at')[:50]
    return render(request, 'auditlogs/list.html', {'logs': logs})