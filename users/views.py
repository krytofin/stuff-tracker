from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from .models import User
import json


def userRegister(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not User.objects.filter(email=cd["username"]).exists():
                if not User.objects.filter(email=cd["email"]).exists():
                    user = User.objects.create_user( # type: ignore
                        username=cd["username"],
                        email=cd["email"],
                        password=cd["password1"],
                    )
                    user.save()
                    login(request, user)
                    messages.success(
                        request,
                        _("You successfully registered a user"),
                        extra_tags="success",
                    )
                    return redirect("tracker:home")
                else:
                    messages.error(
                        request, _("This Email is exists"), extra_tags="warning"
                    )
            else:
                messages.error(
                    request, _("This Username is exists"), extra_tags="warning"
                )
        else:
            er = json.loads(form.errors.as_json())
            for e in er:
                messages.error(request, er[e][0]["message"], "warning")
    return render(request, "users/register.html", {"form": form})


def userLogin(request):
    if not request.user.is_active:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if User.objects.filter(username=cd["username"]).exists():
                    user = authenticate(
                        request, username=cd["username"], password=cd["password"]
                    )
                    if user is not None:
                        login(request, user)
                        messages.success(
                            request, _("logged in successfully"), extra_tags="success"
                        )
                        return redirect("tracker:home")
                    else:
                        messages.error(
                            request,
                            _("your username Or Password is wrong"),
                            extra_tags="warning",
                        )
                else:
                    messages.error(
                        request,
                        _("No account created with this username"),
                        extra_tags="warning",
                    )
                    return redirect("users:login")
            else:
                messages.error(
                    request,
                    _("Please enter your information correctly"),
                    extra_tags="warning",
                )
        else:
            form = LoginForm()
        return render(request, "users/login.html", {"form": form})
    else:
        return redirect("tracker:home")


@login_required()
def LogoutPage(request):
    logout(request)
    messages.success(request, _("You Logged Out successfully"), extra_tags="success")
    return redirect("tracker:home")
