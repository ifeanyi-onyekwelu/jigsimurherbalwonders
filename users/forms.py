from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
)
from django.contrib.auth.models import User
from .models import UserProfile, Address
from django.contrib.auth import authenticate


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your registered email address",
                "autofocus": True,
            }
        ),
        label="Email Address",
    )

    def get_users(self, email):
        """Override to support both email and username lookup"""
        # First try to find by email
        users = User.objects.filter(email__iexact=email, is_active=True)
        if not users.exists():
            # If no email match, try username
            users = User.objects.filter(username__iexact=email, is_active=True)
        return (u for u in users if u.has_usable_password())


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your username or email",
                "autofocus": True,
            }
        ),
        label="Username or Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        ),
        label="Password",
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Keep me signed in",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow login with email or username
        self.fields["username"].help_text = "You can use your username or email address"

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Check if it's an email
        if "@" in username:
            try:
                # Try to find user by email
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                pass
        return username


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
            }
        ),
        help_text="We will use this email for account verification and updates",
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your first name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your last name",
            }
        ),
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Choose a unique username",
            }
        ),
        help_text="Letters, digits and @/./+/-/_ only. 150 characters or fewer.",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Create a strong password",
            }
        ),
        help_text="Your password should be at least 8 characters long",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm your password",
            }
        ),
        help_text="Enter the same password as before, for verification",
    )
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="I agree to the Terms of Service and Privacy Policy",
    )
    newsletter_subscription = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Subscribe to our newsletter for health tips and special offers",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            # Update user profile with newsletter preference
            # The profile is automatically created by the post_save signal
            try:
                profile = user.profile
            except:
                # Profile should exist due to signal, but create if somehow missing
                from .models import UserProfile

                profile = UserProfile.objects.get_or_create(user=user)[0]

            profile.newsletter_subscription = self.cleaned_data.get(
                "newsletter_subscription", False
            )
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
            "date_of_birth",
            "avatar",
            "bio",
            "newsletter_subscription",
        ]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "newsletter_subscription": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["first_name"].widget.attrs["class"] = "form-control"
            self.fields["last_name"].widget.attrs["class"] = "form-control"
            self.fields["email"].widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update User model fields
            user = profile.user
            user.first_name = self.cleaned_data.get("first_name", "")
            user.last_name = self.cleaned_data.get("last_name", "")
            user.email = self.cleaned_data.get("email", "")
            user.save()
            profile.save()
        return profile


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "type",
            "first_name",
            "last_name",
            "company",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "phone_number",
            "is_default",
        ]
        widgets = {
            "type": forms.Select(attrs={"class": "form-select"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "address_line_1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line_2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
