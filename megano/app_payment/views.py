import random
import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView

from megano.app_goods.forms import OrderPaymentForm
from megano.app_order.models import Order
from megano.app_goods.utils import order_created


@csrf_exempt
@require_POST
def payment(request):
    card_number = request.POST.get('card_number', None)
    errors_list = [
        'Ошибка сервера',
        'Банк отклонил платеж',
        'Неправильный номер счета',
        'Недостаточно средств',
        'Счет заблокирован'
    ]
    status = ''
    code = 1
    if int(card_number) % 2 or card_number[-1] == '0':
        status = random.choice(errors_list)
        code = 2
    response = {
        'status': status,
        'code': code
    }
    return JsonResponse(response)


class OrderPayment(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderPaymentForm
    template_name = 'app_orders/payment.html'
    raise_exception = True

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.owner != self.request.user:
            raise PermissionDenied
        return object

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        form = OrderPaymentForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.info(request, 'Ждём подтверждения оплаты от платёжной системы.')
            time.sleep(2)
            order_created(object.id)
            return HttpResponseRedirect(reverse('order_detail', args=[object.id]))
        return super().form_invalid(form)