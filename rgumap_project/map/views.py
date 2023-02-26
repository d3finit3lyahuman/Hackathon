import requests
import json
import os
from django.shortcuts import render
from django.contrib import messages

# Create your views here.


def home(request, matching_results=None):
    context = {'matching_results': matching_results}
    return render(request, 'map/home.html', context)




def getMapData(request):

    url = 'https://rgumap-7c428-default-rtdb.europe-west1.firebasedatabase.app/Campus.json'
    response = requests.get(url)

    # Checking if the response is successful.
    if response.status_code == 200:

        data = response.json()

        messages.success(
            request, f'Data retrieved successfully!')

        return render(request, 'map/location.html', {'data': data})

    else:

        return render(request, 'map/location.html', {'data': None})


def get_campus_data():

    # if in production, use campus.json instead of the url

    # check if in production
    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'rgumap_project.settings.production':
        with open('campus.json') as f:
            data = json.load(f)
            campus_data = {}
    else:
        url = 'https://rgumap-7c428-default-rtdb.europe-west1.firebasedatabase.app/Campus.json'
        response = requests.get(url)
        data = json.loads(response.text)
        campus_data = {}

    if 'School' in data:
        for school in data['School']:
            for key in school:
                campus_data[key] = school[key]

    return campus_data


def search_campus(request):
    campus_data = get_campus_data()

    query = request.GET.get('q')
    results = []

    if query and campus_data:
        for school in campus_data:
            for room in campus_data[school]['Rooms']:
                # print(room)

                if query in room.keys():
                    result = room[query]
                    # print(room)
                    # print(query)
                    print(result)
                    # result = str(result)
                    results.append(result)

                    return home(request, matching_results=result)

                else:
                    result = None



    # matching_results = results if query else None

    return home(request, matching_results=result)



