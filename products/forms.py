from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["rating", "title", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=ProductReview.RATING_CHOICES, attrs={"class": "form-select"}
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Review title"}
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your review here...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].empty_label = "Select a rating"
