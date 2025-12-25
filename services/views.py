from django.shortcuts import render, get_object_or_404
from .models import Service
from django.contrib.auth.decorators import login_required
from .forms import StatusCheckForm
@login_required
def check_status(request):
    result = None
    if request.method == 'POST':
        form = StatusCheckForm(request.POST)
        if form.is_valid():
            app_no = form.cleaned_data['application_no']
            
            # --- MOCK LOGIC START (Replace with API later) ---
            last_digit = int(app_no[-1]) if app_no[-1].isdigit() else 0
            
            if last_digit == 1:
                status = "Registered"
                color = "green"
                message = "Congratulations! This trademark is officially registered."
            elif last_digit == 2:
                status = "Objected"
                color = "red"
                message = "The registry has raised an objection. Contact us immediately to file a reply."
            else:
                status = "Pending Processing"
                color = "yellow"
                message = "Your application is currently under review by the registry."
            # --- MOCK LOGIC END ---

            result = {
                'app_no': app_no,
                'status': status,
                'color': color,
                'message': message
            }
    else:
        form = StatusCheckForm()

    return render(request, 'services/status.html', {'form': form, 'result': result})
@login_required
def service_detail(request, slug):
    # Fetch the specific service or show 404 error if not found
    service = get_object_or_404(Service, slug=slug)
    
    return render(request, 'services/service_detail.html', {
        'service': service
    })