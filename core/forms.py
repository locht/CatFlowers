from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
# from allauth.account.forms import SignupForm #ADD nay vao roi chinh trong forms tai khoan, mat khau,...

PAYMENT_CHOICES = (
    ('S', 'Thẻ tín dụng'),
    ('P', 'Ví điện tử')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)  # duong
    shipping_address2 = forms.CharField(required=False)  # so nha
    shipping_country = CountryField(
        blank_label='(select country)').formfield(
            required=False,
            widget=CountrySelectWidget(attrs={
                'class': 'custom-select d-block w-100'
            }))  # thanh pho
    # district = forms.TextInput()  # quan
    # town = forms.TextInput()  # phuong
    shipping_zipcode = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)  # duong
    billing_address2 = forms.CharField(required=False)  # so nha
    billing_country = CountryField(
        blank_label='(select country)').formfield(
            required=False,
            widget=CountrySelectWidget(attrs={
                'class': 'custom-select d-block w-100'
            }))
    billing_zipcode = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholer': 'Mã khuyến mại',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
