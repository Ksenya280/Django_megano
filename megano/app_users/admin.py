from django.contrib import admin
from .models import Profile, Payment


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'avatar']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'number_card']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Profile, ProfileAdmin)
