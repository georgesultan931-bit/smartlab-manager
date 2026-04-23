from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import AuditLog


@login_required
def auditlog_list(request):
    logs = AuditLog.objects.select_related('user').all()
    paginator = Paginator(logs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'auditlogs/auditlog_list.html', {'page_obj': page_obj})
