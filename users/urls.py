from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm

app_name = "users"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("addresses/", views.addresses, name="addresses"),
    path("addresses/add/", views.add_address, name="add_address"),
    path("addresses/<int:address_id>/edit/", views.edit_address, name="edit_address"),
    path(
        "addresses/<int:address_id>/delete/",
        views.delete_address,
        name="delete_address",
    ),
    path("orders/", views.order_history, name="order_history"),
    # Password reset URLs
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            html_email_template_name="registration/password_reset_email_html.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/users/password-reset/done/",
            from_email="JigsimurHerbal <noreply@jigsimurherbal.com>",
            form_class=CustomPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/users/password-reset-complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
