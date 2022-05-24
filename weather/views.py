from email import message
import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):

    appid = '89d5ef2beb667d8e1c86317ddd6bba5a'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=' + appid

    err_msg = ''
    message = ''
    message_class = ''

    if(request.method == 'POST'):
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()
                if res['cod'] == 200:
                    form.save()
                else: 
                    err_msg = 'Город не найден'
            else:
                err_msg = 'Город уже добавлен'

            if err_msg:
                message = err_msg
                message_class = 'alert-danger'
            else:
                message = 'Город добавлен'
                message_class = 'alert-success'
    # print(err_msg)

    form = CityForm()
    
    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': int(res["main"]["temp"]),
            'flike' : int(res["main"]["feels_like"]),
            'desc': res["weather"][0]["description"].capitalize(),
            'icon': res["weather"][0]["icon"]
        }
        
        all_cities.append(city_info)
    
    context = {
        'all_info': all_cities, 
        'form': form,
        'message' : message,
        'message_class' : message_class
    }
    print(message_class)
    
    return render(request, 'weather/index.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('home')