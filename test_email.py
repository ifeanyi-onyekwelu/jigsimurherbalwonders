#!/usr/bin/env python
"""
Test email configuration for JigsimurHerbal
Run this script to test if email is working properly
"""
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jigsimurherbal.settings")
django.setup()

from jigsimurherbal.email_utils import EmailService


def test_basic_email():
    """Test basic email functionality"""
    try:
        print("🧪 Testing basic email configuration...")
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

        from django.core.mail import send_mail

        # Send test email
        send_mail(
            subject="JigsimurHerbal - Email Configuration Test",
            message="This is a test email to verify the email configuration is working properly.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["ifeanyionyekwelu786@gmail.com"],  # Send to yourself
            fail_silently=False,
        )
        print("✅ Basic email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Basic email failed: {str(e)}")
        return False


def test_order_email():
    """Test order notification email"""
    try:
        print("🧪 Testing order email functionality...")

        EmailService.send_order_notification(
            subject="Test Order Notification",
            message="This is a test order notification email.",
            recipient_list=["ifeanyionyekwelu786@gmail.com"],
        )
        print("✅ Order email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Order email failed: {str(e)}")
        return False


def test_support_email():
    """Test support email"""
    try:
        print("🧪 Testing support email functionality...")

        EmailService.send_support_email(
            subject="Test Support Email",
            message="This is a test support email.",
            recipient_list=["ifeanyionyekwelu786@gmail.com"],
        )
        print("✅ Support email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Support email failed: {str(e)}")
        return False


def display_email_config():
    """Display current email configuration"""
    print("\n📧 Current Email Configuration:")
    print("=" * 50)
    print(f"📬 Contact Email: {getattr(settings, 'CONTACT_EMAIL', 'Not configured')}")
    print(f"📦 Orders Email: {getattr(settings, 'ORDERS_EMAIL', 'Not configured')}")
    print(f"🎧 Support Email: {getattr(settings, 'SUPPORT_EMAIL', 'Not configured')}")
    print(f"🤖 NoReply Email: {getattr(settings, 'NOREPLY_EMAIL', 'Not configured')}")
    print(f"⚙️  Server Email: {getattr(settings, 'SERVER_EMAIL', 'Not configured')}")
    print("=" * 50)


if __name__ == "__main__":
    print("🚀 JigsimurHerbal Email Test Suite")
    print("=" * 50)

    display_email_config()

    # Run tests
    tests_passed = 0
    total_tests = 3

    if test_basic_email():
        tests_passed += 1

    if test_order_email():
        tests_passed += 1

    if test_support_email():
        tests_passed += 1

    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print(
            "🎉 All email tests passed! Your email configuration is working correctly."
        )
    else:
        print("⚠️  Some email tests failed. Please check your email configuration.")
        print("\n💡 Next steps:")
        print("1. Verify your email credentials in .env file")
        print("2. Create the missing email accounts on your hosting provider")
        print("3. Ensure all email passwords are correct")
