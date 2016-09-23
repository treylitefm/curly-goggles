from __future__ import unicode_literals

from django.db import models
from ..login_register.models import User

class PokeManager(models.Manager):
    def poke(self, session_user_id, user_id):
        response = {}
        response['errors'] = []
        if session_user_id == user_id:
            response['errors'].append('User can not poke him/herself')
        else:
            session_user = User.objects.get(id=session_user_id)
            receiving_user = User.objects.get(id=user_id)
            poke = self.create(sending_poke=session_user, receiving_poke=receiving_user)
            response['poke'] = poke

        return poke


class Poke(models.Model):
    receiving_poke = models.ForeignKey(User, related_name='receiving_poke')
    sending_poke = models.ForeignKey(User, related_name='sending_poke')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = PokeManager()

    class Meta:
        db_table = 'pokes'
