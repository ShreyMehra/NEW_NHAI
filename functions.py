import json, ast
import geocoder
from math import radians, cos, sin, asin, sqrt

file_state = open('final_state_wise.json', 'r')
data_state = json.load(file_state)

file_highway = open('final_highway_wise.json', 'r')
data_highway = json.load(file_highway)

file_location = open('final_location_wise.json', 'r')
data_location = json.load(file_location)

extra = ["Helpline No. :", 'Emergency Services :',  "Nearest Police Station:", "Highway Administrator (Project Director):", "Project Implementation Unit(PIU)", "Regional Office(RO)", "Representative of Consultant", "Representative of Concessionaire:", "Nearest Hospital(s):"]

def fetch_states():
    return list(data_state.keys())

def fetch_plazas(state):
    return list(data_state[state].keys())

def fetch_highways(state, plaza):
    highway =  list(data_state[state][plaza].keys())[0]
    plaza_id = plaza.split('-')[1]
    length = data_state[state][plaza][highway]['Highway Length']
    plaza_name = data_state[state][plaza][highway][plaza_id]['Plaza Name']
    latitude = data_state[state][plaza][highway][plaza_id]['Latitude']
    longitude = data_state[state][plaza][highway][plaza_id]['Longitude']
    model = data_state[state][plaza][highway][plaza_id]['Model']
    data = json.dumps({key:data_state[state][plaza][highway][plaza_id]['Details'][key] for key in data_state[state][plaza][highway][plaza_id]['Details'] if key not in extra})
    extras = {key:data_state[state][plaza][highway][plaza_id]['Details'][key] for key in data_state[state][plaza][highway][plaza_id]['Details'] if key in extra}
    return highway, length, plaza_name, latitude, longitude, model, data, extras

def fetch_highway_wise():
    return list(data_highway.keys())

def fetch_highway_state(highway):
    state_list = {}
    for data in data_highway[highway]:
        if list(data.keys())[0] not in state_list:
            state_list[list(data.keys())[0]] = 1
        else:
            state_list[list(data.keys())[0]] += 1
    
    return state_list

def fetch_toll_state(highway, state):
    length, id, plaza_name, latitude, longitude, model, details, extras = [], [], [], [], [], [], [], []
    for tolls in data_highway[highway]:
     
        for temp_state, values in tolls.items():
            if temp_state == state:
                length.append(values['Highway Length'])   
                temp_id = list(values.keys())[-1]
                id.append(temp_id)
                data = values[temp_id]
                plaza_name.append(data['Plaza Name'])
                latitude.append(data['Latitude'])
                longitude.append(data['Longitude'])
                model.append(data['Model'])
                detail = json.dumps({key:data['Details'][key] for key in data['Details'] if key not in extra})
                help = {key:data['Details'][key] for key in data['Details'] if key in extra}
                details.append(detail)
                extras.append(help)
                
    return length, id, plaza_name, latitude, longitude, model, details, extras  

def haversine(lat1, lon1, lat2, lon2, radius):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r <= radius

def fetch_loc(loc):
    g = geocoder.bing(loc, key='At3xjpo2p2JIt2jmdhhTegFLVF6YtETmcfdn17poSPeLOof_emkySFGoZ0PUWUjm')
    results = g.json
    if results is not None:
        return results['lat'], results['lng']
    else:
        return None

def fetch_location(loc, radius):
    coordinate = fetch_loc(loc)
    if coordinate is None:
        return False
    lat, lng = coordinate
    all_toll_lat_lng = [ast.literal_eval(a) for a in data_location.keys()]
    list_of_close_tolls_lat_lng = [(lng1, lat1) for (lng1, lat1) in all_toll_lat_lng if lat1 != 'NOT AVAILABLE' and  lng1 != 'NOT AVAILABLE' and haversine(lat1, lng1, lat, lng, radius)]
    
    if len(list_of_close_tolls_lat_lng) == 0:
        return False
    
    state, highway_name, highway_length, id, plaza_name, model, details, extras = [], [], [], [], [], [], [], []
    for toll in list_of_close_tolls_lat_lng:
        data = data_location[str(toll)] 
        state.append(data['State_Name'])
        name = list(data.keys())[0]
        highway_name.append(list(data.keys())[0])
        highway_length.append(data[list(data.keys())[0]]['Highway Length'])
        temp_id = temp_id = list(data[list(data.keys())[0]])[-1]
        id.append(temp_id)
        data = data[name][temp_id]
        plaza_name.append(data['Plaza Name'])
        model.append(data['Model'])
        detail = json.dumps({key:data['Details'][key] for key in data['Details'] if key not in extra})
        help = {key:data['Details'][key] for key in data['Details'] if key in extra}
        details.append(detail)
        extras.append(help)

    return state, highway_name, highway_length, id, plaza_name, model, details, extras


    