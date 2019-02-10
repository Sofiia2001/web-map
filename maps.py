import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm


def reading_from_file(path, year):
    '''
    (str, str) -> dict

    Function returns a dictionary with locations and movies of a needed year

    e.g. {'LOCATIONS': ['Nashville, Tennessee, USA', 'Spiderhouse Cafe, Austin, Texas, USA'],
    'MOVIES': ['#2WheelzNHeelz', '#ATown']}
    '''
    dictionary = {}
    additional = ''

    with open(path, encoding = 'utf-8', errors = 'ignore') as file:
        for line in file.readlines():
            location = ''
            movie = ''
            if line.startswith('"') and year in line:
                try:
                    if '{' and '}' in line:
                        additional = ' ' + line[line.index('{') : line.index('}') + 1]
                        line = line[:line.index('{')] + line[line.index('}') + 1 :]
                except:
                    pass
                location = line[line.index(')') + 1 : ].replace('\t', '').replace('\n', '')
                if '(' and ')' in location:
                    location = location[:location.index('(')]

                movie = line[line.index('"') + 2 : line.index('(') - 1].replace('"', '') + additional

                dictionary['LOCATIONS'] = dictionary.get('LOCATIONS', [])
                dictionary['LOCATIONS'].append(location)
                dictionary['MOVIES'] = dictionary.get('MOVIES', [])
                dictionary['MOVIES'].append(movie)

    return dictionary


def location_coordinates(location):
    '''
    str -> list

    Function converts location into its coordinates
    '''
    geolocator = Nominatim(timeout = 100)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 0.5)
    loc = geolocator.geocode(location)
    if loc:
        coordinates = [loc.latitude, loc.longitude]
        return coordinates


def place_check(place, data):
    '''
    (list, dictionary) -> bool

    Function checks if place input by user is in collected data
    '''
    for loc in data['LOCATIONS']:
        if place in loc.lower():
            return True


def counting(places, data):
    '''
    (list, dict) -> list(list)

    Function counts how many movies were filmed in each country input by user
    '''
    counter_lst = [[place, 0] for place in places if place_check(place, data)]
    for loc in data['LOCATIONS']:
        for el in counter_lst:
            if el[0] in loc.lower():
                el[1] += 1
    return counter_lst


def button_color(num):
    '''
    int -> str

    Function checks the amount of movies in each country to color the buttons in special color
    If amount is less than 5, the color is red
    If amount is from 5 to 10 - pink
    If more - green
    '''
    if 0 < num < 5:
        col = 'red'
    elif 5 <= num <= 10:
        col = 'pink'
    elif num > 10:
        col = 'green'
    return col


def map_formation(year, data, counted):
    '''
    (str, dict, list(list)) -> None

    Function creates a map with three layers depending on the amount of movies filmed in countries
    '''
    map = folium.Map(location = [49.817545, 24.023932],
                     zoom_start = 3)

    MAX_ITERATIONS = 100
    fg_loc = folium.FeatureGroup(name = "{}'s movies filming location".format(year))
    fg_color = folium.FeatureGroup(name = 'Colored buttons by amount of movies in a country')
    fg_circle = folium.FeatureGroup(name = 'Country with the biggest amount of movies')
    tooltip = 'Click me!'

    locations = data['LOCATIONS']
    movies = data['MOVIES']
    amount_lst = [place[1] for place in counted]

    try:
        for i in tqdm(range(len(locations))):
            for place in counted:
                if location_coordinates(locations[i]):

                    fg_loc.add_child(folium.Marker(location = location_coordinates(locations[i]),
                                                  popup = movies[i],
                                                  icon = folium.Icon(),
                                                  tooltip = tooltip))

                    if place[1] == max(amount_lst):
                        fg_circle.add_child(folium.CircleMarker(location = location_coordinates(place[0]),
                                                                radius = 50,
                                                                popup = place[0] + ' is a country with the biggest'
                                                                                   ' amount of movies',
                                                                color = '#3186cc',
                                                                fill = True,
                                                                fill_color = '#91a6b7'))


                    if place[0] in locations[i].lower():
                        color = button_color(place[1])
                        fg_color.add_child(folium.Marker(location = location_coordinates(locations[i]),
                                                         popup = movies[i],
                                                         icon = folium.Icon(color = color),
                                                         tooltip = tooltip))
                    else:
                        continue

            if i == MAX_ITERATIONS:
                break
    except:
        pass


    map.add_child(fg_loc)
    map.add_child(fg_color)
    map.add_child(fg_circle)

    map.add_child(folium.LayerControl())

    map.save('FilmMap.html')



if __name__ == '__main__':
    places = []

    while True:
        year = str(input('Please, input a year you want to get the location of movies from: '))
        num = int(input('Enter the number of countries you want to compare (at least two): '))

        number = num

        while number > 0:
            place = input('Please, now enter those countries with enters: ')
            if type(place) != str:
                print('You entered wrong data, try again!')
                continue
            else:
                places.append(place.lower())
                number -= 1

        data = reading_from_file('locations.list', year)
        counted = counting(places, data)

        if 0 < int(year) < 2020 and num > 1:
            map_formation(year, data, counted)
            break
        else:
            print('You entered wrong data, try again!')
            continue


