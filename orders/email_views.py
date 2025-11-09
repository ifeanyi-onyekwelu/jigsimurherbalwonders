from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from orders.models import Order
from django.contrib.auth.models import User
import uuid

# Email preview views for testing templates


@staff_member_required
def email_preview_index(request):
    """Admin view to list all available email templates for preview"""
    email_templates = {
        "Order Emails": [
            {"name": "Order Confirmation", "url": "orders:preview_order_confirmation"},
            {"name": "Payment Received", "url": "orders:preview_payment_received"},
            {"name": "Order Shipped", "url": "orders:preview_order_shipped"},
            {"name": "Order Delivered", "url": "orders:preview_order_delivered"},
        ],
        "Support Emails": [
            {
                "name": "Support Request Received",
                "url": "orders:preview_support_received",
            },
            {"name": "Support Response", "url": "orders:preview_support_response"},
        ],
        "Newsletter Emails": [
            {"name": "Newsletter Welcome", "url": "orders:preview_newsletter_welcome"},
        ],
    }

    return render(
        request,
        "admin/email_preview_index.html",
        {
            "title": "Email Template Previews",
            "email_templates": email_templates,
        },
    )


@staff_member_required
def preview_order_confirmation(request):
    """Preview order confirmation email template"""
    # Get a sample order or create sample data
    sample_order = get_sample_order()

    context = {
        "order": sample_order,
        "website_url": request.build_absolute_uri("/").rstrip("/"),
    }

    return render(request, "emails/orders/order_confirmation.html", context)


@staff_member_required
def preview_payment_received(request):
    """Preview payment received email template"""
    sample_order = get_sample_order()
    sample_order.payment_confirmed_at = timezone.now()

    context = {
        "order": sample_order,
        "website_url": request.build_absolute_uri("/").rstrip("/"),
    }

    return render(request, "emails/orders/payment_received.html", context)


@staff_member_required
def preview_order_shipped(request):
    """Preview order shipped email template"""
    sample_order = get_sample_order()
    sample_order.shipped_at = timezone.now()
    sample_order.tracking_number = "JH2024001234567"
    sample_order.shipping_carrier = "Nigeria Post Service"
    sample_order.estimated_delivery_date = timezone.now().date()

    context = {
        "order": sample_order,
        "website_url": request.build_absolute_uri("/").rstrip("/"),
        "tracking_url": f"https://tracking.example.com/{sample_order.tracking_number}",
    }

    return render(request, "emails/orders/order_shipped.html", context)


@staff_member_required
def preview_order_delivered(request):
    """Preview order delivered email template"""
    sample_order = get_sample_order()
    sample_order.delivered_at = timezone.now()

    context = {
        "order": sample_order,
        "website_url": request.build_absolute_uri("/").rstrip("/"),
    }

    return render(request, "emails/orders/order_delivered.html", context)


@staff_member_required
def preview_support_received(request):
    """Preview support request received email template"""
    sample_user = get_sample_user()

    context = {
        "user": sample_user,
        "ticket_number": "JIGSIM-2024-001",
        "subject": "Question about product usage",
        "message": "Hello, I recently purchased your Immune Boost supplement and I wanted to know the best time of day to take it. Should I take it with or without food? Thank you!",
        "priority": "Normal",
        "created_at": timezone.now(),
        "website_url": request.build_absolute_uri("/").rstrip("/"),
    }

    return render(request, "emails/support/support_received.html", context)


@staff_member_required
def preview_support_response(request):
    """Preview support response email template"""
    sample_user = get_sample_user()

    context = {
        "user": sample_user,
        "ticket_number": "JIGSIM-2024-001",
        "subject": "Question about product usage",
        "resolved_at": timezone.now(),
        "support_agent": "Sarah from JigsimurHerbal Support",
        "response_time": "2 hours",
        "response_message": """Thank you for your question about our Immune Boost supplement!

For optimal absorption and effectiveness, we recommend taking the Immune Boost supplement:

• **Best Time**: In the morning with or after breakfast
• **With Food**: Yes, taking it with food helps reduce any potential stomach sensitivity
• **Dosage**: Follow the instructions on the bottle (typically 1-2 capsules daily)
• **Consistency**: Take it at the same time each day for best results

The natural ingredients in our Immune Boost blend work gradually to support your immune system, so you may notice benefits after 2-3 weeks of consistent use.

If you have any other questions or concerns, please don't hesitate to reach out. We're here to support your wellness journey!""",
        "website_url": request.build_absolute_uri("/").rstrip("/"),
    }

    return render(request, "emails/support/support_response.html", context)


@staff_member_required
def preview_newsletter_welcome(request):
    """Preview newsletter welcome email template"""
    sample_user = get_sample_user()

    context = {
        "user": sample_user,
        "website_url": request.build_absolute_uri("/").rstrip("/"),
    }

    return render(request, "emails/newsletter/welcome.html", context)


def get_sample_order():
    """Create a sample order object for email previews"""

    class SampleOrderItem:
        def __init__(self, product_name, quantity, price):
            self.product = type("obj", (object,), {"name": product_name})()
            self.quantity = quantity
            self.product_price = price
            self.total_price = quantity * price

    class SampleOrder:
        def __init__(self):
            self.id = 1
            self.order_number = "JH2024001234"
            self.created_at = timezone.now()
            self.billing_first_name = "John"
            self.billing_last_name = "Doe"
            self.shipping_first_name = "John"
            self.shipping_last_name = "Doe"
            self.shipping_company = ""
            self.shipping_address_line_1 = "123 Wellness Street"
            self.shipping_address_line_2 = "Apartment 4B"
            self.shipping_city = "Lagos"
            self.shipping_state = "Lagos State"
            self.shipping_postal_code = "100001"
            self.shipping_country = "Nigeria"
            self.shipping_phone = "+234 802 345 6789"
            self.payment_method = "bank_transfer"
            self.subtotal = 25000.00
            self.shipping_cost = 2000.00
            self.tax_amount = 0.00
            self.total_amount = 27000.00
            self.payment_reference = ""
            self.payment_confirmed_at = None
            self.shipped_at = None
            self.delivered_at = None
            self.tracking_number = ""
            self.shipping_carrier = ""
            self.estimated_delivery_date = None

        def get_payment_method_display(self):
            return "Bank Transfer"

        def get_shipping_method_display(self):
            return "Standard Shipping"

    sample_order = SampleOrder()

    # Create sample order items
    sample_items = [
        SampleOrderItem("Immune Boost Capsules", 2, 8500.00),
        SampleOrderItem("Energy Blend Tea", 1, 6500.00),
        SampleOrderItem("Stress Relief Tincture", 1, 10000.00),
    ]

    # Mock the items relationship
    sample_order.items = type("obj", (object,), {"all": lambda: sample_items})()

    return sample_order


def get_sample_user():
    """Create a sample user object for email previews"""

    class SampleUser:
        def __init__(self):
            self.first_name = "Jane"
            self.last_name = "Smith"
            self.email = "jane.smith@example.com"

    return SampleUser()


# Newsletter management views


@login_required
def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == "POST":
        # Handle newsletter subscription logic here
        messages.success(request, "Successfully subscribed to our newsletter!")
        return redirect("products:home")

    return render(request, "newsletter/subscribe.html")


@login_required
def newsletter_unsubscribe(request, token=None):
    """Handle newsletter unsubscription"""
    if request.method == "POST":
        # Handle newsletter unsubscription logic here
        messages.info(request, "You have been unsubscribed from our newsletter.")
        return redirect("products:home")

    context = {
        "token": token,
    }
    return render(request, "newsletter/unsubscribe.html", context)


@login_required
def email_preferences(request):
    """Manage email preferences"""
    if request.method == "POST":
        # Handle email preferences update logic here
        messages.success(request, "Email preferences updated successfully!")

    # Sample preferences for now
    preferences = {
        "newsletter": True,
        "order_updates": True,
        "promotional_offers": True,
        "product_recommendations": False,
    }

    context = {
        "preferences": preferences,
    }

    return render(request, "users/email_preferences.html", context)
