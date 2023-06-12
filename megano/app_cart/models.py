from django.db import models
from app_order.models import Product
from app_users.models import Profile


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_product(self, profile: Profile, quantity: int):
        total_cost = int(quantity) * int(self.product.price)
        Cart.objects.update_or_create(
            profile=profile, total_cost=int(total_cost), total_count=quantity, product=self
        )

    def get_cart_items(self):
        return CartItem.objects.filter(profile=self.profile)

    def get_count_cart_items(self):
        return CartItem.objects.filter(profile=self.profile).count()

    def update_quantity(self, quantity: int):
        self.quantity = quantity
        self.save()

    def delete_product(self):
        self.delete()


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    total_cost = models.PositiveIntegerField(blank=True, null=True)
    total_count = models.PositiveIntegerField(blank=True, null=True)

    def set_total_cost(self, total_cost: int):
        self.total_cost = total_cost
        self.save()