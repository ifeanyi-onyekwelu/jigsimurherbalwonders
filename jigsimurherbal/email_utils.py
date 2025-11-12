"""
Email utilities for JigsimurHerbal
Handles different types of emails with different sender addresses
"""

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailService:
    """Service class to handle different types of emails"""

    @staticmethod
    def send_order_notification(subject, message, recipient_list, html_message=None):
        """Send order-related emails (payment confirmations, order updates)"""
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_support_email(subject, message, recipient_list, html_message=None):
        """Send customer support emails"""
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_system_email(subject, message, recipient_list, html_message=None):
        """Send system emails (password resets, notifications)"""
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_newsletter_email(subject, message, recipient_list, html_message=None):
        """Send newsletter and marketing emails"""
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_order_confirmation(order, customer_email):
        """Send order confirmation email"""
        subject = f"Order Confirmation - #{order.order_number}"

        # Render HTML template
        html_message = render_to_string(
            "emails/order_confirmation.html",
            {
                "order": order,
                "customer_email": customer_email,
            },
        )

        # Plain text version
        plain_message = strip_tags(html_message)

        return EmailService.send_order_notification(
            subject=subject,
            message=plain_message,
            recipient_list=[customer_email],
            html_message=html_message,
        )

    @staticmethod
    def send_payment_received_notification(order, admin_emails=None):
        """Send notification to admin when payment is received"""
        if admin_emails is None:
            # Extract email from DEFAULT_FROM_EMAIL if it has format "Name <email>"
            from_email = settings.DEFAULT_FROM_EMAIL
            if "<" in from_email and ">" in from_email:
                email_part = from_email.split("<")[1].split(">")[0]
                admin_emails = [email_part]
            else:
                admin_emails = [from_email]

        subject = f"Payment Received - Order #{order.order_number}"
        message = f"""
Payment has been received for order #{order.order_number}.

Customer: {order.billing_first_name} {order.billing_last_name}
Email: {order.user.email if order.user else 'Guest'}
Amount: ₦{order.total_amount:,}
Payment Method: {order.payment_method}

Please process the order accordingly.
        """

        return EmailService.send_order_notification(
            subject=subject, message=message, recipient_list=admin_emails
        )


# Convenience functions for easy importing
def send_order_email(subject, message, recipient_list, html_message=None):
    return EmailService.send_order_notification(
        subject, message, recipient_list, html_message
    )


def send_support_email(subject, message, recipient_list, html_message=None):
    return EmailService.send_support_email(
        subject, message, recipient_list, html_message
    )


def send_system_email(subject, message, recipient_list, html_message=None):
    return EmailService.send_system_email(
        subject, message, recipient_list, html_message
    )
