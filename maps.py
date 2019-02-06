import folium
import geocoder


def reading_from_file(path):
    lst = []
    additional = ''

    with open(path, encoding = 'utf-8', errors = 'ignore') as file:
        for line in file.readlines():
            if line.startswith('"'):
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
    coordinates = [float(coor) for coor in geocoder.yandex(location).latlng]
    return coordinates


def map_formation(year, data):
    map = folium.Map(location = [49.817545, 24.023932],
                     zoom_start = 3)

    featuregroup = folium.FeatureGroup(name = 'Location by year')

    for line in data:
        if year in line:
            try:
                featuregroup.add_child(folium.Marker(location = location_coordinates(line[2]),
                                           popup = line[0],
                                           icon = folium.Icon()))
            except:
                pass

    map.add_child(featuregroup)
    map.save('FilmMap.html')


if __name__ == '__main__':
    year = str(input('Please, input a year you want to get the location of movies from: '))
    data = reading_from_file('loc.list')
    map_formation(year, data)
