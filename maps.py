import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm


def reading_from_file(path, year):
    lst = []
    additional = ''

    with open(path, encoding = 'utf-8', errors = 'ignore') as file:
        for line in file.readlines():
            if line.startswith('"') and year in line:
                try:
                    if '{' and '}' in line:
                        additional = ' ' + line[line.index('{') : line.index('}') + 1]
                        line = line[:line.index('{')] + line[line.index('}') + 1 :]
                except:
                    pass

                lst.append([line[line.index('"') + 2 : line.index('(') - 1].replace('"', '') + additional,
                                  line[line.index('(') + 1 : line.index(')')],
                                  line[line.index(')') + 1 : ].replace('\t', '').replace('\n', '')])

    for info in lst:
        if '(' and ')' in info[2]:
            info[2] = info[2][:info[2].index('(')]

    return lst


def location_coordinates(location):
    geolocator = Nominatim(timeout = 100)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 0.5)
    loc = geolocator.geocode(location)
    coordinates = [loc.latitude, loc.longitude]
    return coordinates


def marker_color():
    pass


def place_check(place, data):
    i = 0
    for place in places:
        if place in data[i][2].lower():
            return True
        i += 1
        if i == len(data):
            break


def map_formation(year, data, places):
    map = folium.Map(location = [49.817545, 24.023932],
                     zoom_start = 3)

    featuregroup = folium.FeatureGroup(name = 'Location by year')

    for line in tqdm(data):
        for place in places:
            if year in line and place_check(place, data):
                try:
                    featuregroup.add_child(folium.Marker(location = location_coordinates(line[2]),
                                            popup = year + ' year\n' + line[0],
                                            icon = folium.Icon()))
                except:
                    pass

    map.add_child(featuregroup)
    map.save('FilmMap.html')


if __name__ == '__main__':
    places = []
    year = str(input('Please, input a year you want to get the location of movies from: '))
    num = int(input('Enter the number of places you want to compare (at least two): '))
    while num > 0:
        place = str(input('Please, now enter those places with enters (city/country): '))
        places.append(place.lower())
        num -= 1
    data = reading_from_file('loc.list', year)
    map_formation(year, data, places)
