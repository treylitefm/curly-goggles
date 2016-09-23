from django.shortcuts import redirect,render
from django.core.urlresolvers import reverse
from django.db.models import Count
from ..login_register.models import User
from .models import Poke

def index(request):
    if 'user_id' not in request.session:
        return redirect(reverse('login_register:index'))

    pokes = Poke.objects.filter(receiving_poke_id=request.session['user_id'])
    count_unique_pokes = []
    for p in pokes:
        count_unique_pokes.append(p.sending_poke_id)

    context = {
        'auth_user': User.objects.get(id=request.session['user_id']),
        'users': User.objects.exclude(id=request.session['user_id']),
        'poked_by_total': len(set(count_unique_pokes)) #tried a gazillion different orm queries, but i cant get the syntax quite right; ultimately, this is the query i want to execute: select receiving_poke_id,count(distinct sending_poke_id) from pokes where receiving_poke_id=2 group by receiving_poke_id;
    } 

    return render(request, 'pokes/index.html', context)

def poke(request, user_id):
    if 'user_id' not in request.session:
        return redirect(reverse('login_register:index'))
    print request.session['user_id'],'poking',user_id
    Poke.objects.poke(request.session['user_id'], user_id)
    return redirect(reverse('pokes:index'))
