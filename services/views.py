from django.shortcuts import render, get_object_or_404
from .models import Service
from django.contrib.auth.decorators import login_required
from core.models import TrademarkApplication
from .forms import StatusCheckForm
@login_required
def check_status(request):
    application = None
    error = None
    
    if request.method == "POST":
        # User ne search button dabaya
        app_no = request.POST.get('application_number').strip()
        
        if app_no:
            try:
                # Database mein dhundo (Case insensitive search)
                application = TrademarkApplication.objects.get(application_number__iexact=app_no)
            except TrademarkApplication.DoesNotExist:
                error = "Application Number not found. Please check and try again."
        else:
            error = "Please enter an Application Number."

    return render(request, 'services/status.html', {'application': application, 'error': error})
@login_required
def service_detail(request, slug):
    # Fetch the specific service or show 404 error if not found
    service = get_object_or_404(Service, slug=slug)
    
    return render(request, 'services/service_detail.html', {
        'service': service
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.utils import generate_application_number
from .forms import NewTrademarkForm
from core.models import Service # Import Service model

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.utils import generate_application_number
from .forms import NewTrademarkForm
from core.models import Service # Import zaroori hai

@login_required
def new_application(request):
    # 1. URL se slug uthao
    pre_selected_slug = request.GET.get('service')
    initial_data = {}
    
    # 2. Agar URL mein service hai, to DB se dhundo
    if pre_selected_slug:
        try:
            service_obj = Service.objects.get(slug=pre_selected_slug)
            # Service Title ko form ke liye set karo
            initial_data = {'service_type': service_obj.title}
            print(f"✅ Service Found: {service_obj.title}") # Terminal me dikhega
        except Service.DoesNotExist:
            print(f"❌ Service Not Found for slug: {pre_selected_slug}")

    if request.method == 'POST':
        form = NewTrademarkForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.application_number = generate_application_number()
            application.user = request.user
            application.filing_date = timezone.now().date()
            application.status = 'received'
            
            # Agar user ne service type change nahi kiya (readonly hai waise)
            # toh wo POST data se apne aap save ho jayega
            
            application.save()
            return redirect('dashboard')
    else:
        # 3. Initial Data Form me inject karo
        form = NewTrademarkForm(initial=initial_data)

    return render(request, 'services/new_application.html', {'form': form})