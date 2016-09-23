from django.shortcuts import redirect,render
from django.core.urlresolvers import reverse
from django.db.models import Count
from ..login_register.models import User
from .models import Poke

def index(request):
    print request.session['user_id'], 'session object'
    if 'user_id' not in request.session:
        return redirect(reverse('login_register:index'))
    context = {
        'auth_user': User.objects.get(id=request.session['user_id']),
        'users': User.objects.exclude(id=request.session['user_id']),
        'poked_by_total': User.objects.filter(id=request.session['user_id']).values('sending_poke__sending_poke_id').annotate(total=Count('sending_poke__sending_poke_id'))
    } 

    print context['poked_by_total'][0]['total']

    return render(request, 'pokes/index.html', context)

def poke(request, user_id):
    if 'user_id' not in request.session:
        return redirect(reverse('login_register:index'))
    print request.session['user_id'],'poking',user_id
    Poke.objects.poke(request.session['user_id'], user_id)
    return redirect(reverse('pokes:index'))
