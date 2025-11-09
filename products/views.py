from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Category, ProductReview
from .forms import ProductReviewForm


def home(request):
    """Home page view with featured products"""
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]

    context = {
        "featured_products": featured_products,
        "categories": categories,
    }
    return render(request, "products/home.html", context)


def product_list(request):
    """Product listing page with search and filtering"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)

    # Search functionality
    search_query = request.GET.get("search")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(short_description__icontains=search_query)
        )

    # Category filtering
    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Price filtering
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort_by = request.GET.get("sort", "-created_at")
    if sort_by in ["name", "-name", "price", "-price", "created_at", "-created_at"]:
        products = products.order_by(sort_by)

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories_with_selection = []
    for category in categories:
        categories_with_selection.append(
            {"category": category, "is_selected": category.slug == category_slug}
        )

    context = {
        "page_obj": page_obj,
        "categories": categories_with_selection,
        "search_query": search_query,
        "selected_category": category_slug,
        "sort_by": sort_by,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(id=product.id)[:4]

    # Reviews
    reviews = product.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    review_form = ProductReviewForm()

    # Check if user has already reviewed this product
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()

    context = {
        "product": product,
        "related_products": related_products,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "review_form": review_form,
        "user_has_reviewed": user_has_reviewed,
    }
    return render(request, "products/product_detail.html", context)


def category_detail(request, slug):
    """Category detail page with products"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_available=True)

    # Sorting
    sort_by = request.GET.get("sort", "-created_at")
    if sort_by in ["name", "-name", "price", "-price", "created_at", "-created_at"]:
        products = products.order_by(sort_by)

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
        "sort_by": sort_by,
    }
    return render(request, "products/category_detail.html", context)


@login_required
def add_review(request, slug):
    """Add a product review"""
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            # Check if user has already reviewed this product
            existing_review = ProductReview.objects.filter(
                product=product, user=request.user
            ).first()

            if existing_review:
                messages.error(request, "You have already reviewed this product.")
            else:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, "Your review has been added successfully!")
        else:
            messages.error(request, "Please correct the errors below.")

    return redirect("products:product_detail", slug=slug)


def search_suggestions(request):
    """AJAX endpoint for search suggestions"""
    query = request.GET.get("q", "")
    suggestions = []

    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(short_description__icontains=query),
            is_available=True,
        )[:10]

        suggestions = [
            {
                "name": product.name,
                "url": product.get_absolute_url(),
                "price": str(product.price),
                "image": product.image.url if product.image else "",
            }
            for product in products
        ]

    return JsonResponse({"suggestions": suggestions})
