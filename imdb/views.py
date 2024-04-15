import requests
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import pandas as pd
import time

def weekly_top(request):

    url = "https://www.imdb.com/chart/top"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url,headers=headers)
    
    soup = BeautifulSoup(response.content, 'html.parser')

    top_movies = []
    for row in soup.select('tbody.lister-list tr'):
        movie_name = row.find("td",class_='ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable').find('a').get_text()

    return HttpResponse("Test Successful")