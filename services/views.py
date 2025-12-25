from django.shortcuts import render
from services.models import Service

def home(request):
    # Fetch active services, limited to 6 for the homepage
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, 'core/index.html', {'services': services})