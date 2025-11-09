def cart_items_count(request):
    """Context processor for cart items count"""
    from .views import get_or_create_cart

    cart = get_or_create_cart(request)
    return {"cart_items_count": cart.total_items}
