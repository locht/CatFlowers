from django.db import models

from django.conf import settings
from django.shortcuts import reverse, get_object_or_404
from django.db.models import Sum
from django_countries.fields import CountryField

# Create your models here.
CATEGORY_CHOICES = (
    ('S', 'NAM'),
    ('SW', 'NỮ'),
    ('OW', 'TRẺ EM'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Item(models.Model):
    title = models.CharField(max_length=100)  # TieuDe
    price = models.IntegerField()  # gia ban san pham
    discount_price = models.IntegerField(
        blank=True, null=True)  # giam gia ban san pham
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=2)  # the loai
    # nhan(new / bestseller ...)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()  # mieu ta
    image = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "slug": self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={
            "slug": self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove_from_cart", kwargs={
            "slug": self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    # la khoa chinh cua bang Item
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # so luong

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)  # user la khoa chinh cua Auth
    ref_code = models.CharField(max_length=30, blank=True, null=True)
    # qhe nhieu nhieu thong qua bang OrderItem
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)  # ngay bat dau
    ordered_date = models.DateTimeField()  # ngay dat hang
    ordered = models.BooleanField(default=False)  # dat hang hay chua dat hang
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)  # Dang giao hang
    received = models.BooleanField(default=False)  # Da nhan hang
    refund_requested = models.BooleanField(default=False)  # yeu cau hoan tien
    refund_granted = models.BooleanField(default=False)  # hoan lai tien

    """
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds

    """

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    # phone = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()  # li do
    accepted = models.BooleanField(default=False)  # da dong y
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
