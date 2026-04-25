from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone

from apps.common import create_audit_log
from apps.tests.models import TestRequest
from .forms import ResultForm
from .models import Result


@login_required
def result_list(request):
    results = Result.objects.select_related(
        'test_request__patient',
        'test_request__test_type',
        'entered_by'
    ).all()

    return render(request, 'results/result_list.html', {'results': results})


@login_required
def result_create(request, test_request_id):
    test_request = get_object_or_404(TestRequest, pk=test_request_id)
    instance = getattr(test_request, 'result', None)

    form = ResultForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        result = form.save(commit=False)
        result.test_request = test_request
        result.entered_by = request.user
        result.save()

        test_request.status = 'completed'
        test_request.completed_at = timezone.now()
        test_request.save(update_fields=['status', 'completed_at'])

        create_audit_log(
            user=request.user,
            action='create' if instance is None else 'update',
            instance=result,
            description=f'Saved result for test request #{test_request.pk}'
        )

        messages.success(request, 'Result saved successfully.')
        return redirect('results:list')

    return render(request, 'results/result_form.html', {
        'form': form,
        'test_request': test_request
    })


@login_required
def result_detail(request, pk):
    result = get_object_or_404(
        Result.objects.select_related(
            'test_request__patient',
            'test_request__test_type',
            'entered_by'
        ),
        pk=pk
    )

    return render(request, 'results/result_detail.html', {'result': result})


@login_required
def result_pdf(request, pk):
    result = get_object_or_404(
        Result.objects.select_related(
            'test_request__patient',
            'test_request__test_type',
            'entered_by'
        ),
        pk=pk
    )

    html_string = render_to_string('results/report_pdf.html', {
        'result': result
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="result_report_{result.pk}.pdf"'

    return response