from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import LoginForm
from django.db import connection

def home(request):
    return render(request, "login.html", context=dict(request.session))

def login(request) :
    cursor = connection.cursor()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            cursor.execute("SET search_path TO public")
            cursor.execute('SELECT * FROM public."auth_user" WHERE "auth_user"."username"=%s AND "auth_user"."password"=%s', [username, password])
            user = cursor.fetchall()
            print(user)
            if len(user) > 0:
                request.session["username"] = user[0][4]
                request.session["email"] = user[0][7]
                # request.session["role"] = user[0][6]
                return redirect('/')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.clear()
    return HttpResponseRedirect("/login")