from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from random import randint

from .models import Code
from .forms import SignUpForm, ConfirmationForm


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.is_active = False
        user.save()
        number = randint(100, 999)
        Code.objects.create(number=number, user=user)
        send_mail(
            subject='Registration confirmation',
            message=f'Ваш код подтверждения регистрации: {number}',
            from_email='kuber01@yandex.ru',
            recipient_list=[f'{user.email}']
        )
        return redirect('confirm')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_confirmation(request):
    form = ConfirmationForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        if len(Code.objects.filter(number=code)) != 0:
            code_obj = Code.objects.get(number=code)
            user = code_obj.user
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            form = ConfirmationForm()
    else:
        form = ConfirmationForm()
    return render(request, 'account_confirmation.html', {'form': form})
