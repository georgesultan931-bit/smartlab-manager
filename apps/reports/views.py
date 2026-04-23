from django.http import HttpResponse

def generate_report(request, pk):
    return HttpResponse("PDF temporarily disabled. The rest of the system is running.")