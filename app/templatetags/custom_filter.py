from django import template
from ..models import Cart

register = template.Library()

@register.filter(name = "currency")
def currency(price):
    return "₹"+str(price)

@register.filter(name = "cartproduct_count")
def currency(user):
    product_count = Cart.objects.filter(user = user).count()
    print(product_count)
    return product_count