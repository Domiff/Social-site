from django.urls import path, reverse_lazy, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from account.views import (
    user_login,
    dashboard,
    register,
    edit,
    users_list,
    user_detail,
    user_follow,
)

app_name = "account"

urlpatterns = [
    # path("login/", user_login, name="login")
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password-change/",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("account:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        PasswordResetView.as_view(success_url=reverse_lazy("account:password_reset_done")),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(success_url=reverse_lazy("account:password_reset_complete")),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # path("", include("django.contrib.auth.urls")),
    path("register", register, name="register"),
    path("", dashboard, name="dashboard"),
    path("edit/", edit, name="edit"),
    path("users/", users_list, name="users_list"),
    path("users/follow/", user_follow, name="user_follow"),
    path("users/<str:username>/", user_detail, name="user_detail"),
]
