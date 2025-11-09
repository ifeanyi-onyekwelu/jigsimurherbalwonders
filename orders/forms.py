from django import forms
from .models import Order
from users.models import Address


class CheckoutForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ("paystack", "Paystack"),
        ("bank_transfer", "Bank Transfer"),
        ("cash_on_delivery", "Cash on Delivery"),
    ]

    use_billing_for_shipping = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        initial="paystack",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        required=True,
    )

    class Meta:
        model = Order
        fields = [
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
            "payment_method",
            "notes",
        ]
        widgets = {
            "billing_first_name": forms.TextInput(attrs={"class": "form-control"}),
            "billing_last_name": forms.TextInput(attrs={"class": "form-control"}),
            "billing_company": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address_line_1": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address_line_2": forms.TextInput(attrs={"class": "form-control"}),
            "billing_city": forms.TextInput(attrs={"class": "form-control"}),
            "billing_state": forms.TextInput(attrs={"class": "form-control"}),
            "billing_postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "billing_country": forms.TextInput(attrs={"class": "form-control"}),
            "billing_phone": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_first_name": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_last_name": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_company": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address_line_1": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address_line_2": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_city": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_state": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_country": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_phone": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # Pre-fill with user information
            self.fields["billing_first_name"].initial = user.first_name
            self.fields["billing_last_name"].initial = user.last_name
            self.fields["shipping_first_name"].initial = user.first_name
            self.fields["shipping_last_name"].initial = user.last_name

            # Get default addresses
            try:
                billing_address = Address.objects.get(
                    user=user, type="billing", is_default=True
                )
                self.fields["billing_first_name"].initial = billing_address.first_name
                self.fields["billing_last_name"].initial = billing_address.last_name
                self.fields["billing_company"].initial = billing_address.company
                self.fields["billing_address_line_1"].initial = (
                    billing_address.address_line_1
                )
                self.fields["billing_address_line_2"].initial = (
                    billing_address.address_line_2
                )
                self.fields["billing_city"].initial = billing_address.city
                self.fields["billing_state"].initial = billing_address.state
                self.fields["billing_postal_code"].initial = billing_address.postal_code
                self.fields["billing_country"].initial = billing_address.country
                self.fields["billing_phone"].initial = billing_address.phone_number
            except Address.DoesNotExist:
                pass

            try:
                shipping_address = Address.objects.get(
                    user=user, type="shipping", is_default=True
                )
                self.fields["shipping_first_name"].initial = shipping_address.first_name
                self.fields["shipping_last_name"].initial = shipping_address.last_name
                self.fields["shipping_company"].initial = shipping_address.company
                self.fields["shipping_address_line_1"].initial = (
                    shipping_address.address_line_1
                )
                self.fields["shipping_address_line_2"].initial = (
                    shipping_address.address_line_2
                )
                self.fields["shipping_city"].initial = shipping_address.city
                self.fields["shipping_state"].initial = shipping_address.state
                self.fields["shipping_postal_code"].initial = (
                    shipping_address.postal_code
                )
                self.fields["shipping_country"].initial = shipping_address.country
                self.fields["shipping_phone"].initial = shipping_address.phone_number
            except Address.DoesNotExist:
                pass
