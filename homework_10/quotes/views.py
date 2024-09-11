from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote, Tag, Author
from django.contrib.auth import authenticate, login
from .forms import QuoteForm, MyUserCreationForm, AuthenticationForm, AuthorForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


def quotes_list(request):
    quotes = Quote.objects.all()

    authors = Author.objects.all()
    tags = Tag.objects.all()
    context = {"quotes": quotes, "authors": authors, "tags": tags}
    return render(request, "quotes/quotes_list.html", context)


def register(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = MyUserCreationForm()
    return render(request, "quotes/register.html", {"form": form})


@login_required()
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            form.save_m2m()
            return redirect("/")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                print("błąd")
                pass
    else:
        form = AuthenticationForm()
    return render(request, "quotes/login.html", {"form": form})


@login_required()
def create_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes:quotes_list")
    else:
        form = AuthorForm()
    return render(request, "quotes/create_author.html", {"form": form})


@login_required()
def load_authors(request):
    if request.method == "POST":
        json_file_path = "quotes/json_data/authors.json"
        with open(json_file_path, "r") as f:
            authors = json.loads(f.read())
            for author in authors:
                born_date = datetime.strptime(
                    author["born_date"], "%B %d, %Y"
                ).strftime("%Y-%m-%d")

                Author.objects.create(
                    fullname=author["fullname"],
                    born_date=born_date,
                    born_location=author["born_location"],
                    description=author["description"],
                )
        return redirect("quotes:quotes_list")


@login_required()
def load_quotes(request):
    if request.method == "POST":
        json_file_path = "quotes/json_data/quotes.json"
        with open(json_file_path, "r") as f:
            quotes = json.loads(f.read())

            for quote_data in quotes:
                author, _ = Author.objects.get_or_create(fullname=quote_data["author"])

                quote, created = Quote.objects.get_or_create(
                    quote=quote_data["quote"], author=author
                )

                if created:

                    for tag_name in quote_data["tags"]:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        quote.tags.add(tag)

        return redirect("quotes:quotes_list")


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "quotes/author_detail.html", {"author": author})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "quotes/password_reset.html"
    email_template_name = "quotes/password_reset_email.html"
    html_email_template_name = "quotes/password_reset_email.html"
    success_url = reverse_lazy("quotes/password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "quotes/password_reset_subject.txt"
