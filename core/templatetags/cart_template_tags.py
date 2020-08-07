from django import template
from core.models import *

register = template.Library()


@register.filter  # hien thi so luong san pham
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
