from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    newsletter_subscription = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()


class Address(models.Model):
    ADDRESS_TYPES = [
        ("billing", "Billing"),
        ("shipping", "Shipping"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.state}"

    def save(self, *args, **kwargs):
        # Ensure only one default address per type per user
        if self.is_default:
            Address.objects.filter(
                user=self.user, type=self.type, is_default=True
            ).update(is_default=False)
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        UserProfile.objects.create(user=instance)
        # Send welcome email to new user
        send_welcome_email(instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved"""
    if hasattr(instance, "profile"):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)


def send_welcome_email(user):
    """Send welcome email to newly registered user"""
    try:
        # Import here to avoid circular imports
        from jigsimurherbal.email_utils import EmailService

        # Build website URL - handle case where request is not available
        website_url = getattr(settings, "SITE_URL", "https://jigsimurherbalwonders.com")

        # Render HTML email template
        html_message = render_to_string(
            "emails/newsletter/welcome.html",
            {
                "user": user,
                "website_url": website_url,
            },
        )

        # Create plain text version
        plain_message = strip_tags(html_message)

        # Send welcome email using newsletter service
        EmailService.send_newsletter_email(
            subject=f"Welcome to JigsimurHerbal, {user.first_name or user.username}! 🌿",
            message=plain_message,
            recipient_list=[user.email],
            html_message=html_message,
        )

        print(f"Welcome email sent to {user.email}")  # For debugging

    except Exception as e:
        # Log error but don't fail user registration if email fails
        print(f"Error sending welcome email to {user.email}: {str(e)}")
        import logging

        logging.error(f"Welcome email failed for {user.email}: {str(e)}")
