from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "product_count", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description")}),
        ("Media", {"fields": ("image",)}),
        ("Settings", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def product_count(self, obj):
        count = obj.products.count()
        url = reverse(
            "admin:products_product_changelist"
        ) + "?category__id__exact={}".format(obj.id)
        return format_html('<a href="{}">{} products</a>', url, count)

    product_count.short_description = "Products"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "is_primary", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                '<img src="{}" style="max-height: 50px; max-width: 100px;">'.format(
                    obj.image.url
                )
            )
        return "No image"

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price_display",
        "stock_status",
        "is_available",
        "is_featured",
        "created_at",
    ]
    list_filter = [
        "category",
        "is_available",
        "is_featured",
        "created_at",
        "price",
        "stock_quantity",
    ]
    search_fields = ["name", "description", "short_description", "ingredients"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    inlines = [ProductImageInline]
    readonly_fields = ["created_at", "updated_at", "image_preview"]
    actions = [
        "mark_as_featured",
        "mark_as_not_featured",
        "mark_as_available",
        "mark_as_unavailable",
    ]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "slug", "category", "short_description")},
        ),
        (
            "Detailed Information",
            {
                "fields": (
                    "description",
                    "weight",
                    "ingredients",
                    "usage_instructions",
                    "benefits",
                    "warnings",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Pricing & Inventory",
            {"fields": ("price", "original_price", "stock_quantity")},
        ),
        ("Media", {"fields": ("image", "image_preview")}),
        ("Status & Features", {"fields": ("is_available", "is_featured")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                '<img src="{}" style="max-height: 100px; max-width: 150px;">'.format(
                    obj.image.url
                )
            )
        return "No image uploaded"

    image_preview.short_description = "Current Image"

    def price_display(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return format_html(
                '<span style="color: green; font-weight: bold;">₦{:,}</span> '
                '<span style="text-decoration: line-through; color: #999;">₦{:,}</span>',
                obj.price,
                obj.original_price,
            )
        return "₦{:,}".format(obj.price)

    price_display.short_description = "Price"

    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return format_html('<span style="color: red;">Out of Stock</span>')
        elif obj.stock_quantity <= 10:
            return format_html(
                '<span style="color: orange;">Low Stock ({})</span>', obj.stock_quantity
            )
        else:
            return format_html(
                '<span style="color: green;">In Stock ({})</span>', obj.stock_quantity
            )

    stock_status.short_description = "Stock Status"

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(
            request, "{} products marked as featured.".format(queryset.count())
        )

    mark_as_featured.short_description = "Mark selected products as featured"

    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(
            request, "{} products unmarked as featured.".format(queryset.count())
        )

    mark_as_not_featured.short_description = "Remove featured status"

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(
            request, "{} products marked as available.".format(queryset.count())
        )

    mark_as_available.short_description = "Mark as available"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(
            request, "{} products marked as unavailable.".format(queryset.count())
        )

    mark_as_unavailable.short_description = "Mark as unavailable"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "user",
        "rating_display",
        "title",
        "is_approved",
        "created_at",
    ]
    list_filter = ["rating", "is_approved", "is_verified_purchase", "created_at"]
    search_fields = ["product__name", "user__username", "title", "comment"]
    date_hierarchy = "created_at"
    actions = ["approve_reviews", "disapprove_reviews"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Review Information",
            {"fields": ("product", "user", "rating", "title", "comment")},
        ),
        ("Status", {"fields": ("is_approved", "is_verified_purchase")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def rating_display(self, obj):
        stars = "⭐" * obj.rating + "☆" * (5 - obj.rating)
        return "{} ({}/5)".format(stars, obj.rating)

    rating_display.short_description = "Rating"

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(
            request, "{} reviews have been approved.".format(queryset.count())
        )

    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(
            request, "{} reviews have been disapproved.".format(queryset.count())
        )

    disapprove_reviews.short_description = "Disapprove selected reviews"


# Customize admin site header and title
admin.site.site_header = "JigsimurHerbal Administration"
admin.site.site_title = "JigsimurHerbal Admin"
admin.site.index_title = "Welcome to JigsimurHerbal Administration"
