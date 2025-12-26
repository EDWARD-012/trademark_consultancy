from .models import Service

def nav_services(request):
    return {
        'all_services': Service.objects.filter(is_active=True).order_by('title')
    }