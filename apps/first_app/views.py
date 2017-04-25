
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
from django.contrib import messages

def index(request):
    context = {
        'all_users': User.objects.all()
    }
    curr_id = request.session['id']
    return render(request, 'first_app/index.html', context)

def register(request):
    if request.method == 'POST':
        if request.POST['register']:
            response_from_models = User.objects.register(request.POST)
            # try:
            if response_from_models['errors']:
                for error in response_from_models['errors']:
                    messages.error(request, error)
                    return redirect('/')
            # except KeyError:
            #     return redirect('/success')

def login(request):
    if request.method == 'POST':
        # try:
        response_from_signin = User.objects.signin(request.POST)
        if response_from_signin['id']:
            for a in response_from_signin['id']:
                request.session['id'] = a.id
            return redirect('/travels')
        else:
            messages.error(request, 'No user in database')
            return redirect ('/')
        # except AttributeError:
            # messages.error(request, 'No user in database')
            # return redirect ('/')

def travels(request):
    curr_id = request.session['id']
    context = {
        'current_user': User.objects.filter(id=curr_id),
        'curr_users_travel_log': Trip.objects.filter(id=curr_id),
        'all_users_travel_log': Trip.objects.all(),
    }
    return render(request, 'first_app/travels.html', context)

def logout(request):
    request.session['id'] = ''
    return redirect('/')


def trip(request, id):
    context = {
        'trip_deets': Trip.objects.filter(id=id),
    }
    for x in context['trip_deets']:
        print x.current_travelers.name
    return render(request, 'first_app/trip.html', context)

def addpage(request):
    context = {
        'current_user': request.session['id']
    }
    return render(request, 'first_app/addpage.html', context)

def add(request):
    if request.method == 'POST':
        response_from_models = Trip.objects.addtrip(request.POST)
        if response_from_models['errors']:
            for error in response_from_models['errors']:
                messages.error(request, error)
                return redirect('/addpage')
        else:
            return redirect('/travels')

def join(request, id):
    if request.method == 'POST':
        Trip.objects.join(request.POST)
        return redirect('/trip/'+ id)

# def session_test_1(request):
#     request.session['test'] = 'Session Vars Worked!'
#     return http.HttpResponseRedirect('done/?session=%s' % request.session.session_key)
#
# def session_test_2(request):
#     return http.HttpResponse('<br>'.join([
#         request.session.session_key,
#         request.GET.get('session'),
#         request.session.get('test', 'Session is Borked :(')
#          ]))
