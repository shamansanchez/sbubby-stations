import networkx as nx
import pprint
import math
import sys
import yaml

g = nx.Graph()

station_yaml = yaml.full_load(open("stations.yml", "r"))
switch_yaml = yaml.full_load(open("switches.yml", "r"))

combined_yaml = {}
combined_yaml.update(station_yaml)
combined_yaml.update(switch_yaml)


def weight(u, v, d):
    ux = combined_yaml[u]["x"]
    uy = combined_yaml[u]["y"]
    uz = combined_yaml[u]["z"]

    vx = combined_yaml[v]["x"]
    vy = combined_yaml[v]["y"]
    vz = combined_yaml[v]["z"]

    w = math.sqrt(pow(vx - ux, 2) + pow(vy - uy, 2) + pow(vz - uz, 2))
    return w


stations = station_yaml.keys()
switches = switch_yaml.keys()

g.add_edge("joshlantis", "farfetchd")
g.add_edge("ksenia", "walker")
g.add_edge("walker", "amazon")
g.add_edge("amazon", "mind_flayer")
g.add_edge("mind_flayer", "roanoke")
g.add_edge("jason", "south")
g.add_edge("hole", "icy_spikes")
g.add_edge("matrejek_meadows", "matrejek_meadows_sheep")
g.add_edge("jungle", "stronghold2point0")
g.add_edge("supermax", "walker_keep")

g.add_edge("sw1", "farfetchd", dir=1)
g.add_edge("sw1", "badlands_hole", dir=2)
g.add_edge("sw1", "jason_valley", dir=3)
g.add_edge("sw1", "isle_of_jason", dir=4)

g.add_edge("sw2", "jason_valley", dir=1)
g.add_edge("sw2", "ksenia", dir=2)
g.add_edge("sw2", "stronghold", dir=3)

g.add_edge("sw3", "welcome_center", dir=2)
g.add_edge("sw3", "icy_spikes", dir=3)
g.add_edge("sw3", "stronghold", dir=4)

g.add_edge("sw4", "welcome_center", dir=1)
g.add_edge("sw4", "roanoke", dir=2)
g.add_edge("sw4", "joshua", dir=3)

g.add_edge("sw5", "joshua", dir=1)
g.add_edge("sw5", "desert", dir=2)
g.add_edge("sw5", "jason", dir=4)

g.add_edge("sw6", "hole", dir=2)
g.add_edge("sw6", "south", dir=3)
g.add_edge("sw6", "matrejek_meadows", dir=4)

g.add_edge("sw7", "matrejek_meadows_sheep", dir=1)
g.add_edge("sw7", "jungle", dir=3)
g.add_edge("sw7", "new_blakeland", dir=4)

g.add_edge("sw8", "desert", dir=1)
g.add_edge("sw8", "supermax", dir=3)
g.add_edge("sw8", "stronghold2point0", dir=4)

out = {}

for station in stations:
    out[station] = {
        "switches": {},
        "pos": {
            "x": station_yaml[station]["x"],
            "y": station_yaml[station]["y"],
            "z": station_yaml[station]["z"],
        },
    }

    for switch in switches:
        a = nx.dijkstra_path(g, station, switch, weight)
        out[station]["switches"][switch] = g.edges[a[-1], a[-2]]["dir"]

print("---")
print(yaml.dump(out))
