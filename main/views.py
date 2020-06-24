import requests
from django.shortcuts import render, redirect
from .models import City, Contact
from django.contrib import messages


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1be6324f259e2d5ad5e3f216c7627890'
    err_msg = ''
    message = ''
    message_class = ''
        
    if request.method == 'POST':
        new_city = request.POST.get('name', '')
        form = City(name=new_city)

    
        existing_city_count = City.objects.filter(name=new_city).count()
        
        if existing_city_count == 0:
            r = requests.get(url.format(new_city)).json()

            if r['cod'] == 200:
                form.save()
            else:
                err_msg = 'City does not exist in the world! Please check your spelling and try again.'
        else:
            err_msg = 'City already exists! Try adding another one.'

        if err_msg:
            message = err_msg
            message_class = 'alert-warning'
        else:
            message = 'City added successfully! Check the weather deets below.'
            message_class = 'alert-success'

    # form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        # print(r)

        city_weather = {
            'city' : city.name,
            'id': city.id,
            'temperature' : r['main']['temp'],
            'feeltemp':r['main']['feels_like'],
            'mintemp':r['main']['temp_min'],
            'maxtemp':r['main']['temp_max'],
            'humidity':r['main']['humidity'],
            'pressure':r['main']['pressure'],
            'windspeed':r['wind']['speed'],
          
            'winddeg':r['wind']['deg'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
     
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'message' : message,
        'message_class' : message_class
    }

    return render(request, 'main/index.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('Home')

def about(request):
    return render(request, 'main/about.html', {})

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        messages.info(request, 'Thanks for connecting with us. Your message has been successfully delivered')
    return render(request, 'main/contact.html', {})