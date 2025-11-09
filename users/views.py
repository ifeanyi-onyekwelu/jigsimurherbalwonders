from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserProfileForm, AddressForm, CustomLoginForm
from .models import Address
from orders.models import Order


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("products:home")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            # Set session to expire when browser is closed
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("products:home")


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect("products:home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            first_name = user.first_name or username

            # Success message with email notification
            messages.success(
                request,
                f"Welcome to JigsimurHerbal, {first_name}! 🌿 "
                f"Your account has been created successfully. "
                f"Check your email for a welcome message with your special discount!",
            )
            return redirect("users:login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    """User profile view"""
    user_profile, created = request.user.profile, False
    if not hasattr(request.user, "profile"):
        from .models import UserProfile

        user_profile = UserProfile.objects.create(user=request.user)
        created = True

    recent_orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]
    addresses = Address.objects.filter(user=request.user)

    context = {
        "user_profile": user_profile,
        "recent_orders": recent_orders,
        "addresses": addresses,
    }
    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request):
    """Edit user profile view"""
    user_profile, created = request.user.profile, False
    if not hasattr(request.user, "profile"):
        from .models import UserProfile

        user_profile = UserProfile.objects.create(user=request.user)
        created = True

    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile, user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def addresses(request):
    """User addresses view"""
    user_addresses = Address.objects.filter(user=request.user)
    return render(request, "users/addresses.html", {"addresses": user_addresses})


@login_required
def add_address(request):
    """Add new address view"""
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect("users:addresses")
    else:
        form = AddressForm()

    return render(request, "users/add_address.html", {"form": form})


@login_required
def edit_address(request, address_id):
    """Edit address view"""
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        messages.error(request, "Address not found.")
        return redirect("users:addresses")

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect("users:addresses")
    else:
        form = AddressForm(instance=address)

    return render(
        request, "users/edit_address.html", {"form": form, "address": address}
    )


@login_required
def delete_address(request, address_id):
    """Delete address view"""
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        address.delete()
        messages.success(request, "Address deleted successfully!")
    except Address.DoesNotExist:
        messages.error(request, "Address not found.")

    return redirect("users:addresses")


@login_required
def order_history(request):
    """User order history view"""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "users/order_history.html", {"orders": orders})
