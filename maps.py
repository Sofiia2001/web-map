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


def place_check(place, data):
    for i in range(len(data)):
        if place in data[i][2].lower():
            return True
        if i == len(data):
            break


def counting(places, data):
    counter_lst = [[place, 0] for place in places if place_check(place, data)]
    for line in data:
        for el in counter_lst:
            if el[0] in line[2].lower():
                el[1] += 1
    return counter_lst



def filling_colour(counted, colours_list):
    counted.sort(key = lambda num: num[1])
    for lst in counted:
        lst.append(colours_list[counted.index(lst)])
        lst.append(colours_list[len(colours_list) - counted.index(lst) - 1])
    return counted


def map_formation(year, data, colours_list):
    map = folium.Map(location = [49.817545, 24.023932],
                     zoom_start = 3)

    fg_loc = folium.FeatureGroup(name = 'Location by year')
    # fg_color = folium.FeatureGroup(name = 'Colored by amount of movies in a country')
    tooltip = 'Click me!'

    for line in tqdm(data):
        for place in colours_list:
            if year in line and place_check(place[0], data):
                try:
                    fg_loc.add_child(folium.Marker(location = location_coordinates(line[2]),
                                            popup = year + ' year\n' + line[0],
                                            icon = folium.Icon(color = place[3]),
                                                   tooltip = tooltip).add_to(map))
                except:
                    pass

                # fg_color.add_child(folium.Choropleth(geo_data = 'loc.list',
                                                    # fill_color = place[2]))


    map.add_child(fg_loc)
    # map.add_child(fg_color)
    # map.add_child(folium.LayerControl())
    map.save('FilmMap.html')


if __name__ == '__main__':
    places = []
    year = str(input('Please, input a year you want to get the location of movies from: '))
    num = int(input('Enter the number of places you want to compare (at least two): '))

    while num > 0:
        place = str(input('Please, now enter those countries with enters: '))
        places.append(place.lower())
        num -= 1

    colours_list = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
         'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
         'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen']
         # 'gray', 'black', 'lightgray']
    data = reading_from_file('loc.list', year)
    counted = counting(places, data)
    colours_list = filling_colour(counted, colours_list)
    map_formation(year, data, colours_list)

#зробити винятки вводу інфи користувачем
# зафарбована карта за к-кстю фільмів на території(окрема функція з порівняннями) (зробити БЕЗ списку кольорів)
# другий шар
# придумати третій
