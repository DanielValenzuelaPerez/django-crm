from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm, RecordForm
from .models import Record
# https://getbootstrap.com/docs/5.3/components/alerts/


def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Username or password not recognized! Try again.')
            return redirect('home')

    return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out...')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered. Welcome!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': record})
    else:
        messages.error(request, 'You must be logged in to view that page.')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.error(request, 'Record deleted successfully...')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to delete records.')
        return redirect('home')
    

def add_record(request):
    form = RecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                new_record = form.save()
                messages.success(request, f'{new_record.first_name} {new_record.last_name} record addedd')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to add new records.')
        return redirect('home')


def edit_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = RecordForm(request.POST or None, instance=record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated record.')
                return redirect('home')
        return render(request, 'edit_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to add new records.')
        return redirect('home')
