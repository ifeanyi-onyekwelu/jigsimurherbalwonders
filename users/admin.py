from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from .models import UserProfile, Address


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Personal Information",
            {"fields": ("phone_number", "date_of_birth")},
        ),
        ("Preferences", {"fields": ("newsletter_subscription",)}),
        ("Profile Image", {"fields": ("avatar",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = (
        "type",
        "first_name",
        "last_name",
        "address_line_1",
        "city",
        "state",
        "is_default",
    )


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, AddressInline)
    list_display = (
        "username",
        "customer_info",
        "contact_info",
        "subscription_status",
        "user_status",
        "join_date",
        "last_activity",
    )
    list_filter = BaseUserAdmin.list_filter + (
        "profile__newsletter_subscription",
        "is_active",
        "is_staff",
    )
    search_fields = BaseUserAdmin.search_fields + ("profile__phone_number",)

    def customer_info(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        if not full_name:
            full_name = "Not provided"
        return format_html(
            "<strong>{}</strong><br><small>{}</small>", full_name, obj.email
        )

    customer_info.short_description = "Customer"

    def contact_info(self, obj):
        try:
            profile = obj.profile
            phone = profile.phone_number or "No phone"
            return format_html("<div>{}</div>", phone)
        except UserProfile.DoesNotExist:
            return "No profile"

    contact_info.short_description = "Contact"

    def subscription_status(self, obj):
        try:
            profile = obj.profile
            if profile.newsletter_subscription:
                return format_html('<span style="color: green;">✓ Subscribed</span>')
            else:
                return format_html('<span style="color: gray;">✗ Not subscribed</span>')
        except UserProfile.DoesNotExist:
            return "No profile"

    subscription_status.short_description = "Newsletter"

    def user_status(self, obj):
        if obj.is_active:
            if obj.is_staff:
                return format_html('<span style="color: blue;">● Staff</span>')
            elif obj.is_superuser:
                return format_html('<span style="color: red;">● Super Admin</span>')
            else:
                return format_html('<span style="color: green;">● Active</span>')
        else:
            return format_html('<span style="color: red;">● Inactive</span>')

    user_status.short_description = "Status"

    def join_date(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    join_date.short_description = "Joined"

    def last_activity(self, obj):
        return obj.last_login.strftime("%Y-%m-%d %H:%M") if obj.last_login else "Never"

    last_activity.short_description = "Last Login"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "address_summary",
        "customer",
        "address_type",
        "location",
        "default_status",
        "created_at",
    ]
    list_filter = ["type", "is_default", "country", "state", "created_at"]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "first_name",
        "last_name",
        "city",
        "state",
        "postal_code",
    ]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Customer", {"fields": ("user",)}),
        ("Address Type", {"fields": ("type", "is_default")}),
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "company", "phone")},
        ),
        (
            "Address Details",
            {
                "fields": (
                    "address_line_1",
                    "address_line_2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def address_summary(self, obj):
        return format_html(
            "<strong>{} {}</strong><br><small>{}</small>",
            obj.first_name,
            obj.last_name,
            f"{obj.address_line_1}, {obj.city}",
        )

    address_summary.short_description = "Address"

    def customer(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:auth_user_change", args=[obj.user.pk]),
            obj.user.username,
        )

    customer.short_description = "Customer"

    def address_type(self, obj):
        colors = {"billing": "#007bff", "shipping": "#28a745"}
        color = colors.get(obj.type, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.type.upper(),
        )

    address_type.short_description = "Type"

    def location(self, obj):
        return f"{obj.city}, {obj.state} {obj.postal_code}"

    location.short_description = "Location"

    def default_status(self, obj):
        if obj.is_default:
            return format_html('<span style="color: green;">✓ Default</span>')
        else:
            return format_html('<span style="color: gray;">○ Regular</span>')

    default_status.short_description = "Default"
