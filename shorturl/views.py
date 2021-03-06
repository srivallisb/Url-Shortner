from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from shorturl.models import UrlTable

import hashlib

# Create your views here.
def createhashvalue(key):
	hash=hashlib.md5(key)
	return hash.hexdigest()[:6]

def home(request):
    return render(request,"home.html")
# Create your views here.
def signup(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		email = request.POST.get("email")

		user = User.objects.create_user(
				username=username,
				password=password,
				email=email
			)
		login(request, user)

		return redirect("/dashboard/")

	return render(request, "signup.html")

def signin(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(username=username, password=password)

		if user != None:
			login(request, user)
			return redirect("/dashboard/")

	return render(request, "signin.html")

def signout(request):
	logout(request)
	return redirect("/")

def dashboard(request):
	user = request.user
	url_instances = UrlTable.objects.filter(user=user)
	return render(request, "dashboard.html", {"url_instances":url_instances})


def create_short_url(request):
	if request.method == "POST":
		long_url = request.POST.get("long_url")
		title = request.POST.get("title")
		
		user = request.user

		short_hash = createhashvalue(long_url.encode())

		url = UrlTable.objects.create(
				long_url=long_url, 
				user=user,
				short_hash=short_hash,
				title=title
			)

		return redirect("/dashboard/")



def redirect_to_long_url(request, hashcode):
        
            url = UrlTable.objects.get(short_hash=hashcode)

            long_url = url.long_url

            url.no_clicks += 1
            url.save()
            
            return redirect(long_url)

        
