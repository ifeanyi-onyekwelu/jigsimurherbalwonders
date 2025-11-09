from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem, ShippingMethod
from .forms import CheckoutForm
from users.models import Address
import json


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    """View cart contents"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    context = {
        "cart": cart,
        "cart_items": cart_items,
    }
    return render(request, "orders/cart.html", context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_or_create_cart(request)

    quantity = int(request.POST.get("quantity", 1))

    # Check stock
    if quantity > product.stock_quantity:
        if request.headers.get("Content-Type") == "application/json":
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Only {product.stock_quantity} items available in stock.",
                }
            )
        messages.error(
            request, f"Only {product.stock_quantity} items available in stock."
        )
        return redirect("products:product_detail", slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": quantity}
    )

    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            if request.headers.get("Content-Type") == "application/json":
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Cannot add more items. Only {product.stock_quantity} available.",
                    }
                )
            messages.error(
                request,
                f"Cannot add more items. Only {product.stock_quantity} available.",
            )
            return redirect("products:product_detail", slug=product.slug)
        cart_item.quantity = new_quantity
        cart_item.save()

    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "success": True,
                "message": f"{product.name} added to cart.",
                "cart_total_items": cart.total_items,
                "cart_total_price": str(cart.total_price),
            }
        )

    messages.success(request, f"{product.name} added to cart.")
    return redirect("products:product_detail", slug=product.slug)


@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    quantity = int(request.POST.get("quantity", 1))

    if quantity <= 0:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        if quantity > cart_item.product.stock_quantity:
            messages.error(
                request, f"Only {cart_item.product.stock_quantity} items available."
            )
            return redirect("orders:cart")

        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated.")

    return redirect("orders:cart")


@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "success": True,
                "message": f"{product_name} removed from cart.",
                "cart_total_items": cart.total_items,
                "cart_total_price": str(cart.total_price),
            }
        )

    messages.success(request, f"{product_name} removed from cart.")
    return redirect("orders:cart")


@login_required
def checkout(request):
    """Checkout view"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("orders:cart")

    # Check stock availability
    for item in cart_items:
        if item.quantity > item.product.stock_quantity:
            messages.error(
                request,
                f"{item.product.name} has only {item.product.stock_quantity} items in stock.",
            )
            return redirect("orders:cart")

    shipping_methods = ShippingMethod.objects.filter(is_active=True)
    user_addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.subtotal = cart.total_price

            # Calculate shipping and total
            shipping_method_id = request.POST.get("shipping_method")
            if shipping_method_id:
                shipping_method = ShippingMethod.objects.get(id=shipping_method_id)
                order.shipping_cost = shipping_method.price

            order.total_amount = order.subtotal + order.shipping_cost + order.tax_amount
            order.save()

            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )

                # Update product stock
                cart_item.product.stock_quantity -= cart_item.quantity
                cart_item.product.save()

            # Clear cart
            cart_items.delete()

            messages.success(
                request, f"Order {order.order_number} placed successfully!"
            )
            return redirect("orders:order_confirmation", order_id=order.id)
    else:
        form = CheckoutForm(user=request.user)

    context = {
        "form": form,
        "cart": cart,
        "cart_items": cart_items,
        "shipping_methods": shipping_methods,
        "user_addresses": user_addresses,
    }
    return render(request, "orders/checkout.html", context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_confirmation.html", {"order": order})


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


def cart_items_count(request):
    """Context processor for cart items count"""
    cart = get_or_create_cart(request)
    return {"cart_items_count": cart.total_items}
