from __future__ import unicode_literals
from django.db import models
import datetime
import re

class User_manager(models.Manager):
    def register(self, postdata):
        error = []
        response_to_views = {}
        if postdata:
            if len(postdata['name']) < 3 and not re.search(r'^\w+$', postdata['name']):
                error.append('Please use three or more letters to write your name.')
                response_to_views['errors'] = error
            elif len(postdata['username']) < 2 and not re.search(r'^\w+$', postdata['username']):
                error.append('Please use three or more letters to write your username.')
                response_to_views['errors'] = error
            elif not re.search(r'^\w+$', postdata.get('password')) < 8 and postdata.get('password') != postdata.get('confirmpw'):
                error.append('Please correct your password fields. You must use at least 8 characters and both passwords must match.')
                response_to_views['errors'] = error
            elif User.objects.filter(username=postdata['username']):
                error.append('This username already exists, please choose another one.')
                response_to_views['errors'] = error
            else:
                self.create(username=postdata['username'],password=postdata['password'],name=postdata['name'])
                error.append('Thank you for registering, please log-in with your new username and password!')
                response_to_views['errors'] = error
        return response_to_views

    def signin(self, postdata):
        response_to_signin = {}
        idea = []
        if postdata:
            if User.objects.filter(username=postdata['username'], password=postdata['password']):
                # User.objects.filter(id=1).update(name= "Shawn")
                a = User.objects.filter(username=postdata['username'])
                for z in a:
                    idea.append(z)
                response_to_signin['id'] = idea
        return response_to_signin

class User(models.Model):
    name = models.CharField(max_length=70)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = User_manager()

class Tripmanager(models.Manager):
    def addtrip(self, postdata):
        error = []
        response_to_views = {}
        if postdata:
            if len(postdata['destination']) == 0:
                error.append('Please include a destination.')
            elif len(postdata['description']) == 0:
                error.append('Please include a description.')
            elif len(postdata['destfrom']) == 0:
                error.append('Please include a date you\'d like to start your travel.')
            elif len(postdata['destto']) == 0:
                error.append('Please include a date you\'d like to end your travel.')
            elif postdata['destto'] < postdata['destfrom']:
                error.append('Please enter the correct travel dates.')
            elif postdata['destto'] == postdata['destfrom']:
                error.append('The from back date should be in the future.')
            elif postdata['destfrom'] < unicode(datetime.date.today()):
                error.append('Please pick a current date.')
            else:
                a = User.objects.filter(id=postdata['user_id'])
                for b in a:
                    self.create(destination=postdata['destination'],description=postdata['description'],destfrom=postdata['destfrom'],destto=postdata['destto'],user_id=b)
            response_to_views['errors'] = error
        return response_to_views

    def join(self, postdata):
        if postdata:
            a = Trip.objects.filter(id=postdata['id'])
            for b in a:
                self.update(current_travelers=postdata['user_id'])

class Trip(models.Model):
    destination = models.CharField(max_length=70, default='')
    description = models.CharField(max_length=200, default='')
    destfrom = models.CharField(max_length=70, default='')
    destto = models.CharField(max_length=70, default='')
    user_id = models.ForeignKey(User, related_name='userid')
    current_travelers = models.ForeignKey(User, related_name='curr_travs', default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Tripmanager()
