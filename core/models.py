from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.text import slugify

# --- APPLICANT TYPE CHOICES ---
TYPE_CHOICES = [
    ('individual', 'Individual'),
    ('startup', 'Startup / Small Enterprise'),
    ('body_corporate', 'Body Corporate / Company'),
    ('trust', 'Trust / NGO'),
    ('partnership', 'Partnership Firm'),
]

# --- STATUS CHOICES ---
STATUS_CHOICES = [
    ('received', 'Application Received'),
    ('sent_to_vienna', 'Sent to Vienna Codification'),
    ('formality_check_pass', 'Formality Check Pass'),
    ('formality_check_fail', 'Formality Check Fail'),
    ('marked_for_exam', 'Marked for Exam'),
    ('objected', 'Objected'),
    ('exam_report_issued', 'Exam Report Issued'),
    ('ready_for_show_cause', 'Ready for Show Cause Hearing'),
    ('advertised', 'Advertised in Journal'),
    ('registered', 'Registered'),
    ('refused', 'Refused'),
    ('withdrawn', 'Withdrawn'),
]

# --- TRADEMARK APPLICATION MODEL ---
class TrademarkApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    application_number = models.CharField(max_length=50, unique=True)
    
    # 🔥 NEW FIELD ADDED HERE 🔥
    service_type = models.CharField(max_length=200, default='New Application')

    trademark_name = models.CharField(max_length=200)
    applicant_name = models.CharField(max_length=200)
    applicant_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='individual')
    company_name = models.CharField(max_length=200, blank=True, null=True, help_text="Required if not Individual")
    trademark_class = models.IntegerField(help_text="Class 1-45")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='received')
    filing_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trademark_name} ({self.application_number})"

    class Meta:
        ordering = ['-updated_at']

    # --- EMAIL TRIGGER LOGIC ---
    def save(self, *args, **kwargs):
        is_new = self.pk is None 
        
        if not is_new:
            try:
                old_instance = TrademarkApplication.objects.get(pk=self.pk)
                if old_instance.status != self.status and self.user and self.user.email:
                    self.send_status_email()
            except TrademarkApplication.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if is_new:
            self.send_new_app_emails()

    # Email 1: Status Update
    def send_status_email(self):
        subject = f"Update on Trademark Application {self.application_number}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [self.user.email]

        context = {
            'user_name': self.user.first_name or self.user.username,
            'app_number': self.application_number,
            'trademark_name': self.trademark_name,
            'new_status': self.get_status_display(),
            'dashboard_link': f"{settings.SITE_URL}/dashboard/"
        }

        html_content = render_to_string('emails/status_update.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        
        try:
            msg.send()
            print(f"✅ Status Update Email sent to {self.user.email}")
        except Exception as e:
            print(f"❌ Failed to send Status email: {e}")

    # Email 2: New Application (User + Admin)
    def send_new_app_emails(self):
        context = {
            'user_name': self.user.first_name or self.user.username,
            'user_email': self.user.email,
            'app_number': self.application_number,
            'trademark_name': self.trademark_name,
            'applicant_name': self.applicant_name,
            'trademark_class': self.trademark_class,
            'filing_date': self.filing_date,
            'dashboard_link': f"{settings.SITE_URL}/dashboard/",
            'admin_link': f"{settings.SITE_URL}/admin/",
        }

        # A. User Email
        if self.user and self.user.email:
            subject_user = f"Application Received: {self.application_number} - Manyan IP"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [self.user.email]

            html_content_user = render_to_string('emails/new_application_user.html', context)
            text_content_user = strip_tags(html_content_user)

            msg_user = EmailMultiAlternatives(subject_user, text_content_user, from_email, to_email)
            msg_user.attach_alternative(html_content_user, "text/html")
            
            try:
                msg_user.send()
                print(f"✅ User Welcome Email sent to: {self.user.email}")
            except Exception as e:
                print(f"❌ User Email Failed: {e}")

        # B. Admin Email
        admin_email = settings.ADMIN_EMAIL 
        subject_admin = f"🔔 NEW LEAD: {self.application_number} ({self.trademark_name})"

        html_content_admin = render_to_string('emails/new_application_admin.html', context)
        text_content_admin = strip_tags(html_content_admin)

        msg_admin = EmailMultiAlternatives(subject_admin, text_content_admin, from_email, [admin_email])
        msg_admin.attach_alternative(html_content_admin, "text/html")
        
        try:
            msg_admin.send()
            print(f"✅ Admin Alert Email sent to: {admin_email}")
        except Exception as e:
            print(f"❌ Admin Email Failed: {e}")


# --- SERVICE MODEL ---
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('business', 'Formation of Business'),
        ('license', 'Licenses & Registration'),
        ('litigation', 'Litigation Services'),
        ('ip', 'Intellectual Property (IP)'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="Auto-generated URL name")
    
    short_description = models.CharField(max_length=300, help_text="Shown on Dashboard", null=True, blank=True)
    detailed_description = models.TextField(help_text="Full details about the service", null=True, blank=True)
    documents_required = models.TextField(help_text="List of documents needed", default="To be discussed")
    price_estimate = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Starts from ₹5000")
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    service_interested = models.CharField(max_length=100, default='General Enquiry')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"