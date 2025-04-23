import json 

def retrieve_map_dict(map_name):
    with open('assets/maps.json', 'r') as file:
        map_data = json.load(file)
        return map_data[map_name]

def retrieve_horse_list():
    with open('assets/horses.json', 'r') as file:
        horse_data = json.load(file)
        return horse_data['horses']