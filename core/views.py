from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Trademark Consultancy Setup Complete. Ready for Phase 2.</h1>")