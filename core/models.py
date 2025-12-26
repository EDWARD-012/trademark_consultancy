from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail  # send_mail add kiya hai
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

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

class TrademarkApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    application_number = models.CharField(max_length=50, unique=True)
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

    # 🔥 UPDATED EMAIL LOGIC 🔥
    def save(self, *args, **kwargs):
        # 1. Pehle check karo: Kya ye entry bilkul nayi hai?
        is_new = self.pk is None 
        
        # 2. Agar ye UPDATE hai (Naya nahi hai), to purana status check karo
        if not is_new:
            try:
                old_instance = TrademarkApplication.objects.get(pk=self.pk)
                # Agar Status badla hai, aur User exist karta hai
                if old_instance.status != self.status and self.user and self.user.email:
                    self.send_status_email()
            except TrademarkApplication.DoesNotExist:
                pass

        # 3. Data ko Database mein Save karo
        super().save(*args, **kwargs)

        # 4. Agar ye NEW entry thi, to Welcome aur Admin mails bhejo
        if is_new:
            self.send_new_app_emails()

    # --- EMAIL 1: Status Update (User ke liye - HTML Template wala) ---
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

    # --- EMAIL 2: New Application (User Confirmation + Admin Alert) ---
    def send_new_app_emails(self):
        # A. Email to USER (Confirmation)
        if self.user and self.user.email:
            subject_user = f"Application Received: {self.application_number}"
            msg_user = f"Dear {self.user.first_name},\n\nWe have received your application for '{self.trademark_name}'.\nYour App ID is: {self.application_number}.\n\nYou can track status on your dashboard.\n\nRegards,\nManyan IP Team"
            
            try:
                send_mail(subject_user, msg_user, settings.DEFAULT_FROM_EMAIL, [self.user.email])
                print(f"✅ Confirmation Email sent to User: {self.user.email}")
            except Exception as e:
                print(f"❌ User Email Failed: {e}")

        # B. Email to ADMIN (Notification)
        # Admin email yahan change kar lena
        admin_email = 'knowsnoone232@gmail.com' 
        
        subject_admin = f"🔔 NEW LEAD: {self.application_number} ({self.trademark_name})"
        msg_admin = f"""
        New Application Received!
        -------------------------
        App Number: {self.application_number}
        Brand Name: {self.trademark_name}
        Applicant: {self.applicant_name}
        Class: {self.trademark_class}
        User Email: {self.user.email if self.user else 'Unknown'}
        
        Please login to Admin Panel to review.
        """
        
        try:
            send_mail(subject_admin, msg_admin, settings.DEFAULT_FROM_EMAIL, [admin_email])
            print(f"✅ Alert Email sent to Admin: {admin_email}")
        except Exception as e:
            print(f"❌ Admin Email Failed: {e}")


def send_new_app_emails(self):
        # Common Context Data for both emails
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

        # A. Email to USER (HTML)
        if self.user and self.user.email:
            subject_user = f"Application Received: {self.application_number} - Manyan IP"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [self.user.email]

            # Render HTML
            html_content_user = render_to_string('emails/new_application_user.html', context)
            text_content_user = strip_tags(html_content_user) # Fallback

            msg_user = EmailMultiAlternatives(subject_user, text_content_user, from_email, to_email)
            msg_user.attach_alternative(html_content_user, "text/html")
            
            try:
                msg_user.send()
                print(f"✅ User Welcome Email sent to: {self.user.email}")
            except Exception as e:
                print(f"❌ User Email Failed: {e}")

        # B. Email to ADMIN (HTML)
        admin_email = 'knowsnoone232@gmail.com' # Change this to your real email later
        subject_admin = f"🔔 NEW LEAD: {self.application_number} ({self.trademark_name})"

        # Render HTML
        html_content_admin = render_to_string('emails/new_application_admin.html', context)
        text_content_admin = strip_tags(html_content_admin)

        msg_admin = EmailMultiAlternatives(subject_admin, text_content_admin, from_email, [admin_email])
        msg_admin.attach_alternative(html_content_admin, "text/html")
        
        try:
            msg_admin.send()
            print(f"✅ Admin Alert Email sent to: {admin_email}")
        except Exception as e:
            print(f"❌ Admin Email Failed: {e}")