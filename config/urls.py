"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, contact, dashboard, submit_lead_ajax, upload_document  # Import contact
from services.views import check_status, service_detail
from services import views as service_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('submit-lead-ajax/', submit_lead_ajax, name='submit_lead_ajax'),
    path('accounts/', include('accounts.urls')),
    path('status/', check_status, name='check_status'),
    path('contact/', contact, name='contact'), # New Path
    path('services/<slug:slug>/', service_detail, name='service_detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('new-application/', service_views.new_application, name='new_application'),
    path('application/<int:app_id>/upload/', upload_document, name='upload_document'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)