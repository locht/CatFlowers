from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from datetime import datetime
from .forms import *
from .models import *

import random
import string
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class HomeView(ListView):
    model = Item
    # tao so luong san pham trong 1 page (10 sp moi qua page moi)
    paginate_by = 4
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(
                self.request, "Đơn hàng của bạn không tồn tại!")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True,
            )
            if shipping_address_qs.exists():
                context.update({
                    'default_shipping_address': shipping_address_qs[0],
                })

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True,
            )
            if billing_address_qs.exists():
                context.update({
                    'default_billing_address': billing_address_qs[0],
                })

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "Bạn không có đơn hàng nào")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        # print(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True,
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "Không có địa chỉ giao hàng mặc định (sẵn có)")
                        return redirect('core:checkout')
                else:
                    print("Người dùng đang nhập địa chỉ giao hàng mới")

                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    # district = form.cleaned_data.get('district')
                    # town = form.cleaned_data.get('town')
                    shipping_zipcode = form.cleaned_data.get(
                        'shipping_zipcode')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zipcode]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zipcode=shipping_zipcode,
                            address_type='S'
                        )  # lay tu models

                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(
                            self.request, "Bạn chưa thêm địa chỉ giao hàng")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the default billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True,
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "Không có địa chỉ thanh toán mặc định (sẵn có)")
                        return redirect('core:checkout')
                else:
                    print("Người dùng đang nhập địa chỉ thanh toán mới")

                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    # district = form.cleaned_data.get('district')
                    # town = form.cleaned_data.get('town')
                    billing_zipcode = form.cleaned_data.get(
                        'billing_zipcode')

                    if is_valid_form([billing_address1, billing_country, billing_zipcode]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zipcode=billing_zipcode,
                            address_type='B'
                        )  # lay tu models

                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(
                            self.request, "Bạn chưa thêm địa chỉ thanh toán")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Thanh toán được chọn không hợp lệ!")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "Bạn không có một đơn đặt hàng nào")
            return redirect("core:order_summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "Bạn vui lòng thêm đầy đủ địa chỉ giao hàng và thanh toán")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = order.get_total()  # int

        try:
            # create user payment 'POST' to Stipe's API
            # customer = stripe.Customer.create(
            #     email=self.request.POST.get('email'),
            #     name=self.request.POST.get('nickname'),
            #     source=self.request.POST.get('stripeToken'),
            # )

            # create payment 'POST' to Stipe's API
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="my first charge"
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount
            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Bạn đã đặt hàng của thành công!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Lỗi giới hạn tỷ lệ!")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Thông số không hợp lệ!")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Không xác thực!")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Lỗi mạng!")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Đã xảy ra lỗi. Bạn đã không bị tính phí. Vui lòng thử lại.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "Một lỗi nghiêm trọng đã xảy ra. Chúng tôi đã được thông báo.")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Thêm sản phẩm thành công")
            return redirect("core:order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Sản phẩm đã được thêm vào giỏ hàng")
            return redirect("core:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "Sản phẩm đã được thêm vào giỏ hàng")
        return redirect("core:order_summary")
    return redirect("core:product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()  # order_item
            messages.info(request, "Sản phẩm đã được xóa khỏi giỏ hàng")
            return redirect("core:order_summary")
        else:
            messages.info(request, "Không có sản phẩm nào trong giỏ hàng")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "Bạn không có đơn hàng nào")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "Số lượng sản phẩm đã giảm đi 1 đơn vị")
                return redirect("core:order_summary")
            else:
                order_item.delete()  # order_item
                messages.info(
                    request, "Sản phẩm đã được xóa khỏi giỏ hàng")
                return redirect("core:order_summary")
        else:
            messages.info(request, "Không có sản phẩm trong giỏ hàng")
            return redirect("core:order_summary", slug=slug)
    else:
        messages.info(request, "Bạn không có đơn hàng nào")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "Phiếu giảm giá này không tồn tại")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(
                    self.request, "Thêm phiếu giảm giá thành công")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "Bạn không có đơn hàng nào")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Yêu cầu của bạn đã được gửi đi")
                return redirect("core:request_refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "Thứ tự này không tồn tại")
                return redirect("core:request_refund")
