from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from account.models import Profile, Contact


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    template_path = "account/login.html"
    context = {"form": form}
    return render(request, template_path, context)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    template_path = "account/dashboard.html"
    context = {"section": "dashboard"}
    return render(request, template_path, context)


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            template_path = "account/register_done.html"
            context = {"new_user": new_user}
            return render(request, template_path, context)
    else:
        user_form = UserRegistrationForm()
    template_path = "account/register.html"
    context = {"user_form": user_form}
    return render(request, template_path, context)


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    template_path = "account/edit.html"
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, template_path, context)


@login_required
def users_list(request: HttpRequest) -> HttpResponse:
    template_path = "account/user/list.html"
    context = {"users": User.objects.filter(is_active=True), "section": "people"}
    return render(request, template_path, context)


@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    template_path = "account/user/detail.html"
    context = {
        "user": get_object_or_404(User, username=username, is_active=True),
        "section": "people",
    }
    return render(request, template_path, context)


@require_POST
@login_required
def user_follow(request: HttpRequest) -> HttpResponse:
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if action and user_id:
        try:
            user = User.objects.get(pk=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})
