from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

# 🔥 CORRECT IMPORTS 🔥
# Models 'core' app ke andar hi hain, isliye .models use karenge
from core.models import TrademarkApplication, Service, Lead 

# Forms aapne 'services' app mein shift kiye the, isliye wahan se import karenge
from services.forms import LeadForm

# --- HOME PAGE VIEW ---
def home(request):
    # 1. Fetch Top 6 Active Services for Display
    services = Service.objects.filter(is_active=True)[:6]
    
    # 2. Handle Lead Form (Consultation Request)
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            # A. Database mein save karo
            form.save()
            
            # B. Email Data Nikalo
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            service = form.cleaned_data.get('service_interested', 'Not Specified')
            user_msg = form.cleaned_data.get('message', '')

            # C. Admin ko Email Bhejo
            subject = f"🔔 New Lead from Website: {name}"
            email_message = f"""
            You have received a new consultation request.
            
            --------------------------------
            Name: {name}
            Phone: {phone}
            Service Interested: {service}
            Message: {user_msg}
            --------------------------------
            
            Please contact them immediately.
            """
            
            try:
                send_mail(
                    subject=subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL], # 🔥 Real Admin Email
                    fail_silently=False,
                )
                print("✅ Email Sent to Admin")
            except Exception as e:
                print(f"❌ Email Sending Failed: {e}")
            
            # D. Success Message
            messages.success(request, "Thank you! We have received your enquiry and will contact you shortly.")
            return redirect('home') # Page refresh par dobara submit hone se rokne ke liye
            
        else:
            messages.error(request, "Please check the form details and try again.")
    else:
        form = LeadForm()

    return render(request, 'core/index.html', {
        'services': services, 
        'form': form
    })

# --- CONTACT PAGE VIEW ---
def contact(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            
            # 🔥 Email Logic for Contact Page too
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            
            send_mail(
                subject=f"📩 Contact Page Enquiry: {name}",
                message=f"Name: {name}\nPhone: {phone}\nMessage: {form.cleaned_data.get('message')}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )

            messages.success(request, "Enquiry Sent! We will call you shortly.")
            return redirect('contact')
    else:
        form = LeadForm()
    
    return render(request, 'core/contact.html', {'form': form})

# --- DASHBOARD VIEW ---
@login_required
def dashboard(request):
    # 1. User ki applications fetch karo
    user_applications = TrademarkApplication.objects.filter(user=request.user).order_by('-filing_date')
    app_count = user_applications.count()
    
    # 2. Services ko categorize karke fetch karo (Active Only)
    services_business = Service.objects.filter(category='business', is_active=True)
    services_license = Service.objects.filter(category='license', is_active=True)
    services_litigation = Service.objects.filter(category='litigation', is_active=True)
    services_ip = Service.objects.filter(category='ip', is_active=True)

    return render(request, 'core/dashboard.html', {
        'user': request.user,
        'applications': user_applications,
        'app_count': app_count,
        # Services Categories passed to template
        'services_business': services_business,
        'services_license': services_license,
        'services_litigation': services_litigation,
        'services_ip': services_ip,
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives # 🔥 Change here
from django.template.loader import render_to_string # 🔥 Change here
from django.utils.html import strip_tags
from django.conf import settings
from django.http import JsonResponse

# Correct Imports
from .models import TrademarkApplication, Service, Lead
from services.forms import LeadForm

# ... (Home, Contact Views same rahenge) ...

# --- AJAX VIEW (Updated for HTML Emails) ---
def submit_lead_ajax(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save() # Save and get instance
            
            # Context Data for Emails
            context = {
                'name': lead.name,
                'phone': lead.phone,
                'email': lead.email,
                'service': lead.service_interested,
                'message': lead.message
            }
            
            # --- 1. SEND ADMIN EMAIL (HTML) ---
            try:
                subject_admin = f"🔔 New Lead: {lead.name} ({lead.service_interested})"
                html_content_admin = render_to_string('emails/callback_admin.html', context)
                text_content_admin = strip_tags(html_content_admin) # Fallback

                msg_admin = EmailMultiAlternatives(subject_admin, text_content_admin, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
                msg_admin.attach_alternative(html_content_admin, "text/html")
                msg_admin.send()
                print("✅ Admin HTML Email Sent")
            except Exception as e:
                print(f"❌ Admin Email Error: {e}")

            # --- 2. SEND USER EMAIL (HTML) ---
            if lead.email:
                try:
                    subject_user = "Callback Request Received - Manyan IP Services"
                    html_content_user = render_to_string('emails/callback_user.html', context)
                    text_content_user = strip_tags(html_content_user) # Fallback

                    msg_user = EmailMultiAlternatives(subject_user, text_content_user, settings.DEFAULT_FROM_EMAIL, [lead.email])
                    msg_user.attach_alternative(html_content_user, "text/html")
                    msg_user.send()
                    print("✅ User HTML Email Sent")
                except Exception as e:
                    print(f"❌ User Email Error: {e}")

            return JsonResponse({'status': 'success', 'message': 'Request Sent! Check your email for confirmation.'})
        
        else:
            return JsonResponse({'status': 'error', 'message': 'Please fix the errors.', 'errors': form.errors})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})