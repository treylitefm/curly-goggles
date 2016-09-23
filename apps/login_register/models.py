from __future__ import unicode_literals
from django.db import models
from re import match
from datetime import datetime
import bcrypt

DATE_INPUT_FORMATS = ('%d-%m-%Y')

class UserManager(models.Manager):
    def register(self, data):
        print 'omarrrrr'

        EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$' 
        NAME_REGEX = r'^[A-z\s]*$'
        errors = []

        if data['name'] == '':
            errors.append('First name can not be blank')
        if len(data['name']) < 2:
            errors.append('First name must be fewer than 2 characters')
        if not match(NAME_REGEX, data['name']):
            errors.append('First name can only contain letters')
        if data['alias'] == '':
            errors.append('Last name can not be blank')
        if len(data['alias']) < 2:
            errors.append('Last name must be fewer than 2 characters')
        if not match(NAME_REGEX, data['alias']):
            errors.append('Last name can only contain letters')
        
        if data['email'] == '':
            errors.append('Email can not be blank')
        if not match(EMAIL_REGEX, data['email']):
            errors.append('Email format invalid')

        if data['password'] == '':
            errors.append('Password can not be blank')
        elif data['password'] != data['password_confirm']:
            errors.append('Passwords must be matching')
        elif data['password'] < 8:
            errors.append('Passwords must be at least 8 characters in length')
        else:
            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        if data['birth_date'] == '':
            errors.append('Birth Date can not be blank')
        birth_date = datetime.strptime(data['birth_date'], '%d/%m/%Y').strftime('%Y-%m-%d')

        if self.filter(email=data['email']):
            errors.append('Email already exists')

        result = {}
        
        if not errors:
            result['created'] = True
            u = User(name=data['name'], alias=data['alias'], email=data['email'], password=password, birth_date=birth_date)
            u.save()
            result['user'] = u
        else:
            result['created'] = False
            result['errors'] = errors

        return result

    def login(self, data):
        u = self.filter(email=data['email'])
        result = {}
    
        if data['password'] != '' and u and u[0].password == bcrypt.hashpw(data['password'].encode('utf-8'), u[0].password.encode('utf-8')):
            result['success'] = True
            u = u[0]
            result['user_id'] = u.id
            result['name'] = u.name
            result['alias'] = u.alias
        else:
            result['success'] = False

        return result


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        db_table = 'users'
