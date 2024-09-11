from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.quotes_list, name="quotes_list"),
    path("register/", views.register, name="register"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("create_author/", views.create_author, name="create_author"),
    path("load_authors/", views.load_authors, name="load_authors"),
    path("load_quotes/", views.load_quotes, name="load_quotes"),
    path("authors/<int:author_id>/", views.author_detail, name="author_detail"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url="reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
