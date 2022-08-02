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


def index(request):
    return render(request, "todo_app/index.html")


def about(request):
    return render(request, "todo_app/about.html")


class LoginRequest(View):
    def get(self, request):
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


def contact(request):
    if request.method == "POST":
        form = MessageForm(request.POST or None)
        if form.is_valid:
            form.save()
            message_list = ContactMessage.objects.all()

            send_mail(
                'message from ' + request.POST['name'],
                request.POST['message'],
                settings.EMAIL_HOST_USER,
                ['dilaratuluce@gmail.com'],
                fail_silently=False
            )

            return render(request, "todo_app/contact.html", {'message_list': message_list})


    else:
        message_list = ContactMessage.objects.all()
        return render(request, "todo_app/contact.html", {'message_list': message_list})



"""
def login_request(request):
    if request.method == "POST":
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
"""

"""
def signin_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/user")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="todo_app/register.html", context={"register_form": form})
"""

#def howitworks(request):
#    return render(request, "todo_app/howitworks.html")


