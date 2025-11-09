from django.urls import path
from . import views, email_views

app_name = "orders"

urlpatterns = [
    # Cart and Order URLs
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "update-cart-item/<int:item_id>/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path(
        "remove-from-cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "order-confirmation/<uuid:order_id>/",
        views.order_confirmation,
        name="order_confirmation",
    ),
    path("order/<uuid:order_id>/", views.order_detail, name="order_detail"),
    # Email Preview URLs (Admin Only)
    path(
        "admin/email-previews/",
        email_views.email_preview_index,
        name="email_preview_index",
    ),
    path(
        "admin/email-previews/order-confirmation/",
        email_views.preview_order_confirmation,
        name="preview_order_confirmation",
    ),
    path(
        "admin/email-previews/payment-received/",
        email_views.preview_payment_received,
        name="preview_payment_received",
    ),
    path(
        "admin/email-previews/order-shipped/",
        email_views.preview_order_shipped,
        name="preview_order_shipped",
    ),
    path(
        "admin/email-previews/order-delivered/",
        email_views.preview_order_delivered,
        name="preview_order_delivered",
    ),
    path(
        "admin/email-previews/support-received/",
        email_views.preview_support_received,
        name="preview_support_received",
    ),
    path(
        "admin/email-previews/support-response/",
        email_views.preview_support_response,
        name="preview_support_response",
    ),
    path(
        "admin/email-previews/newsletter-welcome/",
        email_views.preview_newsletter_welcome,
        name="preview_newsletter_welcome",
    ),
    # Newsletter Management URLs
    path(
        "newsletter/subscribe/",
        email_views.newsletter_subscribe,
        name="newsletter_subscribe",
    ),
    path(
        "newsletter/unsubscribe/",
        email_views.newsletter_unsubscribe,
        name="newsletter_unsubscribe",
    ),
    path(
        "newsletter/unsubscribe/<str:token>/",
        email_views.newsletter_unsubscribe,
        name="newsletter_unsubscribe_token",
    ),
    path("email-preferences/", email_views.email_preferences, name="email_preferences"),
]
