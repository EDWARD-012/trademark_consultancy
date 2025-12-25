from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="URL friendly name (e.g. trademark-registration)")
    short_description = models.TextField(max_length=300, help_text="Shown on homepage cards")
    full_description = models.TextField(help_text="Shown on details page")
    # Using URLField for now to save you from AWS S3/Cloudinary setup headaches immediately
    image_url = models.URLField(max_length=500, blank=True, help_text="Paste an image link here")
    icon_class = models.CharField(max_length=50, default="fa-solid fa-gavel", help_text="FontAwesome class (e.g., fa-solid fa-file-contract)")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title