from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH (login, logout, OTP)
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),

    # MAIN APP
    path('dashboard/', include(('apps.dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('patients/', include(('apps.patients.urls', 'patients'), namespace='patients')),
    path('tests/', include(('apps.tests.urls', 'tests'), namespace='tests')),
    path('results/', include(('apps.results.urls', 'results'), namespace='results')),
    path('reports/', include(('apps.reports.urls', 'reports'), namespace='reports')),
    path('auditlogs/', include(('apps.auditlogs.urls', 'auditlogs'), namespace='auditlogs')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)