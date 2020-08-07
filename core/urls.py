from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from core.views import *
from allauth.account.views import LoginView, SignupView, LogoutView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/',
         remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('add_coupon/', AddCouponView.as_view(), name='add_coupon'),
    path('request_refund/', RequestRefundView.as_view(), name='request_refund'),



    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
