import networkx as nx
import pprint
import math
import sys
import yaml

'''
Function used to calculate distance between two stops
'''
def weight(u, v, d):
    ux = all_coordinates[u]["x"]
    uy = all_coordinates[u]["y"]
    uz = all_coordinates[u]["z"]

    vx = all_coordinates[v]["x"]
    vy = all_coordinates[v]["y"]
    vz = all_coordinates[v]["z"]

    w = math.sqrt(pow(vx - ux, 2) + pow(vy - uy, 2) + pow(vz - uz, 2))
    return w

'''
In this context, a stop is either a station or a switch.
Given properly formatted stop dictionaries, return dictionaries mapping...

stops -> coordinates

AND

stops -> connections

...returning both dictionaries.

'''
def process(data):
    coordinates = {}
    connections = {}

    for stop, stop_data in data.items():
        coordinates[stop] = stop_data['coordinates']
        connections[stop] = stop_data['connections']

    return(coordinates, connections)

# Load YAML from files
station_yaml = yaml.full_load(open("stations.yml", "r"))
switch_yaml = yaml.full_load(open("switches.yml", "r"))

# Process switches, stations into respective coordinates and connections dictionaries
switch_coordinates, switch_connections = process(switch_yaml)
station_coordinates, station_connections = process(station_yaml)

# Create dictionary with all coordinates (primarily for calculating weights)
all_coordinates = {}
all_coordinates.update(station_coordinates)
all_coordinates.update(switch_coordinates)

# Build map from connections dictionaries
g = nx.from_dict_of_lists(station_connections)
g.update(nx.from_dict_of_dicts(switch_connections))

# Create a data structure that maps keys NESW to 1-4, respectively
direction_handler = dict((y,x) for x,y in enumerate(["N", "E", "S", "W"], start=1))

# Calculate the switch configuration required for shortest paths to each station
out = {}
for station, coordinates in station_coordinates.items():
    out[station] = {
        "switches": {},
        "pos": {
            "x": coordinates["x"],
            "y": coordinates["y"],
            "z": coordinates["z"],
        },
    }

    for switch in switch_coordinates.keys():
        a = nx.dijkstra_path(g, station, switch, weight)
        direction = g.edges[a[-1], a[-2]]["dir"]
        out[station]["switches"][switch] = direction_handler[direction]

# Print results
print("---")
print(yaml.dump(out))
