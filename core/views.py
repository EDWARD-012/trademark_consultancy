from django.shortcuts import render, redirect
from django.contrib import messages
from services.models import Service
from leads.forms import LeadForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .models import TrademarkApplication

def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            
            # Simple Email Notification (Prints to console for now)
            send_mail(
                subject=f"New Lead: {form.cleaned_data['name']}",
                message=f"Service: {form.cleaned_data['service']}\nPhone: {form.cleaned_data['phone']}",
                from_email='noreply@trademark.com',
                recipient_list=['admin@trademark.com'],
                fail_silently=True,
            )
            
            messages.success(request, "Thank you! We have received your enquiry and will contact you shortly.")
            return redirect('home') # Prevents double submission on refresh
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LeadForm()

    return render(request, 'core/index.html', {
        'services': services, 
        'form': form
    })

@login_required
def contact(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enquiry Sent! We will call you shortly.")
            return redirect('contact')
    else:
        form = LeadForm()
    
    return render(request, 'core/contact.html', {'form': form})

@login_required
def dashboard(request):
    # 2. Database se User ki applications nikalo (Latest first)
    user_applications = TrademarkApplication.objects.filter(user=request.user).order_by('-filing_date')
    
    # 3. 'applications' key ke saath template ko bhejo
    return render(request, 'core/dashboard.html', {  # Note: Path check kar lena ('core/dashboard.html' ya 'dashboard.html')
        'user': request.user,
        'applications': user_applications 
    })