import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import JsonResponse

# 🔥 Models Import
from .models import TrademarkApplication, Service, Lead, ApplicationDocument

# 🔥 Forms Import
from services.forms import LeadForm, DocumentUploadForm

# Logger setup
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------
# 1. HOME PAGE VIEW
# ----------------------------------------------------------------
def home(request):
    # Top 6 Active Services for Display (General List)
    services = Service.objects.filter(is_active=True)[:6]
    
    # Handle Lead Form Submission (Fallback for non-AJAX)
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            
            # Admin Email Logic
            try:
                subject = f"New Lead from Website: {lead.name}"
                email_message = f"""
                New Lead Received:
                Name: {lead.name}
                Phone: {lead.phone}
                Service: {lead.service_interested}
                Message: {lead.message}
                """
                send_mail(
                    subject, email_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=False
                )
            except Exception:
                pass # Fail silently in fallback
            
            messages.success(request, "Thank you! We have received your enquiry.")
            return redirect('home')
        else:
            messages.error(request, "Please check the form details.")
    else:
        form = LeadForm()

    return render(request, 'core/index.html', {
        'services': services, 
        'form': form
    })

# ----------------------------------------------------------------
# 2. CONTACT PAGE VIEW
# ----------------------------------------------------------------
# core/views.py mein 'contact' function ko replace karein

def contact(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            
            # --- Email Context (Same as Home Page) ---
            context = {
                'name': lead.name,
                'phone': lead.phone,
                'email': lead.email,
                'service': lead.service_interested,
                'message': lead.message
            }

            # --- 1. Send Admin Email (HTML) ---
            try:
                subject_admin = f"🔔 New Contact Enquiry: {lead.name}"
                html_content_admin = render_to_string('emails/callback_admin.html', context)
                text_content_admin = strip_tags(html_content_admin)
                
                msg_admin = EmailMultiAlternatives(subject_admin, text_content_admin, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
                msg_admin.attach_alternative(html_content_admin, "text/html")
                msg_admin.send()
                print("✅ Contact Page: Admin Email Sent")
            except Exception as e:
                print(f"❌ Contact Page Admin Error: {e}")

            # --- 2. Send User Email (HTML) ---
            if lead.email:
                try:
                    subject_user = "We received your message - Manyan IP Services"
                    html_content_user = render_to_string('emails/callback_user.html', context)
                    text_content_user = strip_tags(html_content_user)
                    
                    msg_user = EmailMultiAlternatives(subject_user, text_content_user, settings.DEFAULT_FROM_EMAIL, [lead.email])
                    msg_user.attach_alternative(html_content_user, "text/html")
                    msg_user.send()
                    print("✅ Contact Page: User Email Sent")
                except Exception as e:
                    print(f"❌ Contact Page User Error: {e}")

            messages.success(request, "Enquiry Sent! We will call you shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Please check the form details.")
    else:
        form = LeadForm()
    
    return render(request, 'core/contact.html', {'form': form})

# ----------------------------------------------------------------
# 3. AJAX LEAD SUBMISSION (For Popup Form)
# ----------------------------------------------------------------
def submit_lead_ajax(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            
            # Context for HTML Emails
            context = {
                'name': lead.name,
                'phone': lead.phone,
                'email': lead.email,
                'service': lead.service_interested,
                'message': lead.message
            }
            
            # A. Send Admin Email
            try:
                subject_admin = f"🔔 New Lead: {lead.name} ({lead.service_interested})"
                html_content = render_to_string('emails/callback_admin.html', context)
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject_admin, text_content, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                print(f"Admin Email Error: {e}")

            # B. Send User Email
            if lead.email:
                try:
                    subject_user = "Callback Request Received - Manyan IP Services"
                    html_content = render_to_string('emails/callback_user.html', context)
                    text_content = strip_tags(html_content)
                    msg = EmailMultiAlternatives(subject_user, text_content, settings.DEFAULT_FROM_EMAIL, [lead.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except Exception as e:
                    print(f"User Email Error: {e}")

            return JsonResponse({'status': 'success', 'message': 'Request Sent! Check email for confirmation.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Fix form errors.', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

# ----------------------------------------------------------------
# 4. DASHBOARD VIEW (UPDATED FOR 5 CATEGORIES)
# ----------------------------------------------------------------
@login_required
def dashboard(request):
    # 1. User Applications
    user_applications = TrademarkApplication.objects.filter(user=request.user).order_by('-filing_date')
    app_count = user_applications.count()
    
    # 2. Fetch Services by 5 Categories (Corrected Keys)
    services_formation = Service.objects.filter(category='formation', is_active=True)
    services_license = Service.objects.filter(category='license', is_active=True)
    services_litigation = Service.objects.filter(category='litigation', is_active=True)
    services_ip = Service.objects.filter(category='ip', is_active=True)
    services_global_ip = Service.objects.filter(category='global_ip', is_active=True)

    return render(request, 'core/dashboard.html', {
        'user': request.user,
        'applications': user_applications,
        'app_count': app_count,
        # Passing 5 Context Variables
        'services_formation': services_formation,   # Was 'business' incorrectly
        'services_license': services_license,
        'services_litigation': services_litigation,
        'services_ip': services_ip,
        'services_global_ip': services_global_ip,   # Added this
    })

# ----------------------------------------------------------------
# 5. DOCUMENT UPLOAD VIEW
# ----------------------------------------------------------------
@login_required
def upload_document(request, app_id):
    application = get_object_or_404(TrademarkApplication, id=app_id, user=request.user)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.application = application
            doc.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('upload_document', app_id=app_id)
    else:
        form = DocumentUploadForm()

    uploaded_docs = application.documents.all().order_by('-uploaded_at')

    return render(request, 'core/upload_docs.html', {
        'application': application,
        'form': form,
        'uploaded_docs': uploaded_docs
    })


# core/views.py

from django.shortcuts import get_object_or_404, redirect
from .models import ApplicationDocument

# ... existing imports ...

@login_required
def delete_document(request, doc_id):
    # Document fetch karein
    doc = get_object_or_404(ApplicationDocument, id=doc_id)
    
    # Security Check: Kya ye document current user ki application ka hai?
    if doc.application.user == request.user:
        app_id = doc.application.id  # Redirect ke liye ID save kar lo
        doc.delete()  # 🔥 Delete Database Entry & File
        messages.success(request, "Document deleted successfully.")
        return redirect('upload_document', app_id=app_id)
    else:
        messages.error(request, "Unauthorized action.")
        return redirect('dashboard')