from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})