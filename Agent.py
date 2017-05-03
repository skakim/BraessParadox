from kspmaster import KSP
import random

def route_to_string(route):
    r = ""
    for edge in route[:-1]:
        n = edge.split("-")[0]
        r += n
        r += "->"
    r += route[-1].split("-")[0]
    r += "->"
    r += route[-1].split("-")[1]
    return r

def string_to_route(route):
    s_route = route.split("->")
    r = []
    for i in range(len(s_route[:-1])):
        a = s_route[i] + "-" + s_route[i+1]
        r.append(a)
    return r

class Agent:
    def __init__(self,routes):
        self.table = {}
        for i in routes:
            route = i[0]
            route = route_to_string(route)
            cost = i[1]
            self.table[route] = cost

    def select_route(self):
        min_cost = min(self.table.itervalues())
        min_routes = [k for k in self.table if self.table[k] == min_cost]
        r = random.choice(min_routes)
        return string_to_route(r)