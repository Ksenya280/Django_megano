from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from megano.app_users.models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from forms import AvatarForm


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
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("app_users:login")


class AvatarView(View):
    @login_required
    def user_list(self, request):
        users = User.objects.all()
        return render(request, 'user_list.html', {'users': users})

    @login_required
    def user_detail(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        is_admin = request.user.is_staff
        return render(request, 'user_detail.html', {'user': user, 'is_admin': is_admin})

    @login_required
    def update_avatar(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not request.user.is_staff and user != request.user:
            return redirect(reverse('user_detail', args=[pk]))
        if request.method == 'POST':
            form = AvatarForm(request.POST, request.FILES, instance=user.profile)
            if form.is_valid():
                form.save()
                return redirect(reverse('user_detail', args=[pk]))
        else:
            form = AvatarForm(instance=user.profile)
        return render(request, 'update_avatar.html', {'form': form, 'user': user})





