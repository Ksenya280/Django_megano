from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from .models import Profile
from .forms import Balance
import logging

logger = logging.getLogger(__name__)


class AboutMeView(TemplateView):
    template_name = "app_users/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "app_users/register.html"
    success_url = reverse_lazy("app_users:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        logger.info('A new user has registered.')
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("app_users:login")


def user_form(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = Balance(instance=request.user.profile, data=request.POST)
        if form.is_valid():
            money = form.cleaned_data.get('balance', 0)
            if money > 0:
                user = User.objects.get(pk=request.user.id)
                user.profile.balance += money
            form.save()
            logger.info('Replenishment of the balance')
            return render(request, 'app_users/about-me.html')
    else:
        form = Balance()
    return render(request, "app_users/balance.html", {'form': form})