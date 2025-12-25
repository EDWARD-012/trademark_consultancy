from django.db import models
from django.contrib.auth.models import User

# --- TRADEMARK STATUS CHOICES ---
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
    # Link to a user (Optional: agar client registered hai toh connect kar sakte hain)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Unique Application Number (e.g., 5678901)
    application_number = models.CharField(max_length=50, unique=True)
    
    # Details
    trademark_name = models.CharField(max_length=200)
    applicant_name = models.CharField(max_length=200)
    trademark_class = models.IntegerField(help_text="Class 1-45")
    
    # Status
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='received')
    
    # Dates
    filing_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trademark_name} ({self.application_number})"

    class Meta:
        ordering = ['-updated_at']