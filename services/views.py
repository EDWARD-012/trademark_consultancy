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
from core.utils import generate_application_number # Import our generator
from .forms import NewTrademarkForm

@login_required
def new_application(request):
    if request.method == 'POST':
        form = NewTrademarkForm(request.POST)
        if form.is_valid():
            # 1. Form data uthao par abhi Database mein save mat karo
            application = form.save(commit=False)
            
            # 2. AUTOMATIC ID GENERATE KARO
            application.application_number = generate_application_number()
            
            # 3. Baaki fields auto-fill karo
            application.user = request.user
            application.filing_date = timezone.now().date()
            application.status = 'received' # Default status
            
            # 4. Ab Final Save karo
            application.save()
            
            # 5. Success page ya Dashboard par bhej do
            return redirect('dashboard')
    else:
        form = NewTrademarkForm()

    return render(request, 'services/new_application.html', {'form': form})