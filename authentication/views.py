from django.shortcuts import render, redirect
from authentication import forms
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from fotoblog import settings


#vue base sur une classe
class LoginPage(View):
    form_class = forms.LoginForm
    templates_name = "authentication/login.html"
    def get(self, request):
        form = self.form_class
        message = ""
        return render(request, self.templates_name, context={'form': form, 'message': message})
    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            message = ''
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    message = "Identifiants invalides"
        return render(request, self.templates_name, context={'form': form, 'message': message})


#vue base sur une fonction
def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                message = "Identifiants invalides"

    return render(request, "authentication/login.html", context={'form':form, 'message':message})



def logout_user(request):
    logout(request)
    return redirect('login')

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={'form':form})


def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})