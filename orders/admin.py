from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from .models import Cart, CartItem, Order, OrderItem, ShippingMethod, OrderTracking


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("created_at", "updated_at", "subtotal")
    fields = ("product", "quantity", "subtotal", "created_at")

    def subtotal(self, obj):
        try:
            return "₦{:.2f}".format(obj.get_total_price())
        except (TypeError, AttributeError):
            return "₦0.00"

    subtotal.short_description = "Subtotal"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user__username", "user__email", "session_key"]
    inlines = [CartItemInline]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("created_at", "item_total")
    fields = ("product", "quantity", "product_price", "item_total", "created_at")

    def item_total(self, obj):
        if obj.quantity and obj.product_price:
            return "₦{:.2f}".format(obj.quantity * obj.product_price)
        return "₦0.00"

    item_total.short_description = "Item Total"


class OrderTrackingInline(admin.TabularInline):
    model = OrderTracking
    extra = 0
    readonly_fields = ("created_at",)
    fields = ("status", "description", "created_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_display",
        "customer_info",
        "status_display",
        "payment_display",
        "total_display",
        "order_date",
        "actions_column",
    ]
    list_filter = ["status", "payment_status", "created_at", "updated_at"]
    search_fields = [
        "order_number",
        "user__username",
        "user__email",
        "billing_first_name",
        "billing_last_name",
    ]
    readonly_fields = (
        "id",
        "order_number",
        "created_at",
        "updated_at",
        "order_summary",
    )
    inlines = [OrderItemInline, OrderTrackingInline]
    date_hierarchy = "created_at"
    actions = [
        "mark_as_processing",
        "mark_as_shipped",
        "mark_as_delivered",
        "mark_as_cancelled",
    ]

    fieldsets = (
        (
            "Order Overview",
            {
                "fields": (
                    "id",
                    "order_number",
                    "user",
                    "status",
                    "payment_status",
                    "payment_method",
                    "payment_id",
                    "order_summary",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Billing Information",
            {
                "fields": (
                    "billing_first_name",
                    "billing_last_name",
                    "billing_company",
                    "billing_address_line_1",
                    "billing_address_line_2",
                    "billing_city",
                    "billing_state",
                    "billing_postal_code",
                    "billing_country",
                    "billing_phone",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Shipping Information",
            {
                "fields": (
                    "shipping_first_name",
                    "shipping_last_name",
                    "shipping_company",
                    "shipping_address_line_1",
                    "shipping_address_line_2",
                    "shipping_city",
                    "shipping_state",
                    "shipping_postal_code",
                    "shipping_country",
                    "shipping_phone",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Financial Details",
            {
                "fields": ("subtotal", "shipping_cost", "tax_amount", "total_amount"),
                "classes": ("wide",),
            },
        ),
        (
            "Timeline",
            {
                "fields": ("created_at", "updated_at", "shipped_at", "delivered_at"),
                "classes": ("collapse",),
            },
        ),
        ("Additional Information", {"fields": ("notes",), "classes": ("collapse",)}),
    )

    def order_display(self, obj):
        return format_html(
            "<strong>{}</strong><br><small>ID: {}</small>", obj.order_number, obj.id
        )

    order_display.short_description = "Order"

    def customer_info(self, obj):
        if obj.user:
            return format_html(
                "<strong>{}</strong><br><small>{}</small>",
                "{} {}".format(obj.billing_first_name, obj.billing_last_name),
                obj.user.email,
            )
        return "{} {}".format(obj.billing_first_name, obj.billing_last_name)

    customer_info.short_description = "Customer"

    def status_display(self, obj):
        colors = {
            "pending": "#ffc107",
            "processing": "#007bff",
            "shipped": "#28a745",
            "delivered": "#6c757d",
            "cancelled": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.status.upper(),
        )

    status_display.short_description = "Status"

    def payment_display(self, obj):
        colors = {
            "pending": "#ffc107",
            "paid": "#28a745",
            "failed": "#dc3545",
            "refunded": "#6c757d",
        }
        color = colors.get(obj.payment_status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.payment_status.upper(),
        )

    payment_display.short_description = "Payment"

    def total_display(self, obj):
        if obj.total_amount:
            return "₦{:.2f}".format(obj.total_amount)
        return "₦0.00"

    total_display.short_description = "Total"

    def order_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    order_date.short_description = "Order Date"

    def actions_column(self, obj):
        return format_html(
            '<a class="button" href="{}">View</a>',
            reverse("admin:orders_order_change", args=[obj.pk]),
        )

    actions_column.short_description = "Actions"

    def order_summary(self, obj):
        items = obj.items.all()
        total_items = items.aggregate(total=Sum("quantity"))["total"] or 0
        item_count = items.count()

        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">'
            "<strong>Order Summary:</strong><br>"
            "{} items ({} products)<br>"
            "Subtotal: ₦{:.2f}<br>"
            "Shipping: ₦{:.2f}<br>"
            "Tax: ₦{:.2f}<br>"
            "<strong>Total: ₦{:.2f}</strong>"
            "</div>",
            total_items,
            item_count,
            obj.subtotal or 0,
            obj.shipping_cost or 0,
            obj.tax_amount or 0,
            obj.total_amount or 0,
        )

    order_summary.short_description = "Summary"

    def mark_as_processing(self, request, queryset):
        queryset.update(status="processing")
        self.message_user(
            request, "{} orders marked as processing.".format(queryset.count())
        )

    mark_as_processing.short_description = "Mark as Processing"

    def mark_as_shipped(self, request, queryset):
        from django.utils import timezone

        queryset.update(status="shipped", shipped_at=timezone.now())
        self.message_user(
            request, "{} orders marked as shipped.".format(queryset.count())
        )

    mark_as_shipped.short_description = "Mark as Shipped"

    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone

        queryset.update(status="delivered", delivered_at=timezone.now())
        self.message_user(
            request, "{} orders marked as delivered.".format(queryset.count())
        )

    mark_as_delivered.short_description = "Mark as Delivered"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")
        self.message_user(
            request, "{} orders marked as cancelled.".format(queryset.count())
        )

    mark_as_cancelled.short_description = "Mark as Cancelled"


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price_display",
        "delivery_time",
        "status_display",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at"]

    fieldsets = (
        (
            "Shipping Information",
            {"fields": ("name", "description", "price", "estimated_days")},
        ),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )

    def price_display(self, obj):
        if obj.price:
            return "₦{:.2f}".format(obj.price)
        return "₦0.00"

    price_display.short_description = "Price"

    def delivery_time(self, obj):
        if obj.estimated_days:
            return "{} days".format(obj.estimated_days)
        return "Not specified"

    delivery_time.short_description = "Delivery Time"

    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> Active')
        return format_html('<span style="color: red;">●</span> Inactive')

    status_display.short_description = "Status"
