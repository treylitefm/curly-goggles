from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import User

def index(request):
    if 'user_id' in request.session:
        return redirect(reverse('pokes:index'))
    return render(request, 'login_register/index.html')

def login(request):
    res = User.objects.login(request.POST)
    if res['success']:
        request.session['user_id'] = res['user_id']
    else:
        messages.error(request, 'Invalid Login Credentials', extra_tags='login')
    return redirect(reverse('login_register:index'))

def register(request):
    if request.method == 'POST':
        u = User.objects.register(request.POST)
    if 'errors' in u:
        for e in u['errors']:
            messages.error(request, e, extra_tags='register')
        return redirect(reverse('login_register:index'))
    return redirect(reverse('login_register:index'))

def logout(request):
    request.session.clear()
    return redirect(reverse('login_register:index'))
