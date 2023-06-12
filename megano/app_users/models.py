from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(null=True, blank=False, default=0)
    total_expenses = models.IntegerField(null=True, blank=False, default=0)
    status = models.CharField(null=True, max_length=8, default='Iron')
    agreement_accepted = models.BooleanField(default=False)
    phone = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar")
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return str(self.full_name)


class Payment(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    number_card = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_stock(sender, instance, **kwargs):
    id = instance.id
    user = User.objects.get(id=id)
    Profile.objects.update_or_create(id=id, defaults={"user": user, "email": user.email})

