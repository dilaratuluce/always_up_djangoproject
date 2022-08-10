from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.views import View

from .forms import MessageForm
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings


class Index(View):
    def get(self, request):
        return render(request, "todo_app/index.html")


class LoginRequest(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in, so we redirected you to your personal page.")
            return redirect("/user")
      #      return render(request, "todo_logged_in_app/index.html")

        else:
            form = AuthenticationForm()
            return render(request=request, template_name="todo_app/login.html", context={"login_form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/user")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="todo_app/login.html", context={"login_form": form})


class SigninRequest(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in, so we redirected you to your personal page.")
            return redirect("/user")
        #    return render(request, "todo_logged_in_app/index.html")
        else:
            form = NewUserForm()
            return render(request=request, template_name="todo_app/register.html", context={"register_form": form})

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/user")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
        return render(request=request, template_name="todo_app/register.html", context={"register_form": form})


class HowItWorks(View):
    def get(self, request):
        return render(request, "todo_app/howitworks.html")


class Contact(View):
    def get(self, request):
        return render(request, "todo_app/contact.html")

    def post(self, request):
        form = MessageForm(request.POST or None)
        if form.is_valid():
            form.save()

            send_mail(
                'Contact Form by ' + request.POST['name'],
                request.POST['message'] + '\n\nE-mail: ' + request.POST['email'],
                settings.EMAIL_HOST_USER,
                ['dilaratuluce@gmail.com'],
                fail_silently=False
            )
            messages.success(request, "Thanks for your message! We will reply soon.")
            return render(request, "todo_app/contact.html")
        else:
            messages.error(request, "Couldn't send your message, please fulfill all the fields.")
            return render(request, "todo_app/contact.html")
