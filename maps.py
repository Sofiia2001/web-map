import folium
import geocoder


def reading_from_file(path):
    lst = []

    with open(path, 'r') as file:
        for line in file.readlines():
            if line.startswith('"'):
                if '{' and '}' in line:
                    line = line[ : line.index('{')] + line[line.index('}') + 1 :]

                lst.append([line[line.index('"') + 2 : line.index('(') - 1].replace('"', ''),
                                  line[line.index('(') + 1 : line.index(')')],
                                  line[line.index(')') + 1 : ].replace('\t', '').replace('\n', '')])

    return lst


def location_coordinates(location):
    coordinates = [float(coor) for coor in geocoder.yandex(location).latlng]
    return coordinates


def map_formation(year, data):
    map = folium.Map(location = [49.817545, 24.023932],
                     zoom_start = 3)

    featuregroup = folium.FeatureGroup(name = 'Location by year')

    for line in data:
        if year in line:
            featuregroup.add_child(folium.Marker(location = location_coordinates(line[2]),
                                       popup = line[0],
                                       icon = folium.Icon()))

    map.add_child(featuregroup)
    map.save('FilmMap.html')


if __name__ == '__main__':
    year = str(input('Please, input a year you want to get the location of movies from: '))
    data = reading_from_file('loc.list')
    map_formation(year, data)
