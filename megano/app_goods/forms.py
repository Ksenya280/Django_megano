from django import forms

from megano.app_order.models import Order

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, max_value=21, widget=forms.NumberInput(
            attrs={
                'class': 'Amount-input form-input',
                'min': '1', 'max': '21', 'size': '2',
                'maxlength': '2'
            }
        ),
        label='')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    address = forms.CharField(
        max_length=150, label="Адрес", required=True, widget=forms.Textarea(
            attrs={
                'class': 'form-input',
                'maxlength': '150',
                'data-validate': 'require',
                'autocomplete': 'address',
                'rows': '1'}))
    city = forms.CharField(
        max_length=30, label="Город", required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'maxlength': '30',
                'data-validate': 'require',
                'autocomplete': 'city'}))
    card_number = forms.CharField(
        max_length=11, required=True, label='Номер карты', widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requireCard'}))

    class Meta:
        model = Order
        fields = ['address', 'city', 'delivery_type', 'payment_type', 'card_number']
        widgets = {
            'delivery_type': forms.RadioSelect,
            'payment_type': forms.RadioSelect
        }


class OrderPaymentForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=11, required=True, label='Номер карты', widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'data-validate': 'requireCard'}))

    class Meta:
        model = Order
        fields = ['payment_type', 'card_number']
        widgets = {
            'payment_type': forms.RadioSelect
        }
