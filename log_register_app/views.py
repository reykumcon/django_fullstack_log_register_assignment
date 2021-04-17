from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager
import bcrypt

def index(request):
    return render(request, 'register_login.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        create_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash
            )
        request.session['user_id'] = create_user.id
        return redirect('/success')
    else:
        return redirect('/')

def success(request):
    if 'user_id' in request.session:
        current_user = User.objects.filter(id=request.session['user_id'])
        context = {
            'current_user': current_user[0]
        }
        return render(request, 'success.html', context)
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        current_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = current_user[0].id
        return redirect('/success')
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')
