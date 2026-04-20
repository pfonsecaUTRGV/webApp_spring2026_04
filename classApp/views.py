from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests 
from django.http import JsonResponse

def home(request):
	return render(request, 'home.html',{})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            print("User created successfully")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

@login_required	
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            print("User profile udpated successfully")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, "profile.html", {"u_form": u_form, "p_form":p_form})


def pokedex_view(request):
    pokemon_data = None
    error = None    

    if request.method == "POST":
        pokemon = request.POST.get("pokemon","")

        if pokemon:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                pokemon_data = {

                    "name":data["name"],
                    "id": data["id"],
                    "types":[t["type"]["name"] for t in data ["types"]],
                    "image": data["sprites"]["front_default"],
                }
        else:
            error = "The pokemon does not exist"

    return render(request,"pokedex.html",{
        "pokemon_data":pokemon_data,
        "error": error,})


def hello_API(request):
    data = {

        "message": "Hello World this is my API",
        "name"   : "3340 Software Engineering",
        "date"   : "April 20th 2026",
        "section": "04"
    }

    return JsonResponse(data)