from kspmaster import KSP
import numpy as np
import sys
from numpy import exp
from math import fabs

epsilon = 1.0/sys.maxint #avoid "division by zero" error
fermiK = 10.0

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

def normalize(value, oldmin, oldmax, newmin, newmax):
    newvalue = (((float(value) - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin
    return newvalue

def fermi_mistrust(Px,Py,K):
    delta = -fabs(-(Py - Px))
    w = (1/(1+(exp(-delta/K))))
    w = normalize(w,0.0,0.5,0.0,1.0)
    #print(Px,Py,delta,w)
    return w

class Agent:
    def __init__(self,routes,delta=1.0,learning_p=1.0,forecast=True,resistence=False):
        self.delta = delta
        self.learning_p = learning_p
        self.forecast = forecast
        self.resistence = resistence
        #self.routes_costs = {}
        self.routes_costs_somatories = {}
        self.routes_usage = {}
        for i in routes:
            route = i[0]
            route = route_to_string(route)
            cost = i[1]
            #self.routes_costs[route] = [cost]
            self.routes_costs_somatories[route] = cost
            self.routes_usage[route] = 0
            self.costs_table = []
        self.p_table = self.gen_p_table()

    def gen_p_table(self):
        p_table = {}
        for route in self.routes_costs_somatories.keys():
            v1 = (1.0/(self.routes_costs_somatories[route]+epsilon))
            v2 = 0.0
            for route2 in self.routes_costs_somatories.keys():
                v2 += (1.0/(self.routes_costs_somatories[route2]+epsilon))
            p = v1/v2
            p_table[route] = p
        return p_table

    def update_p_table(self):
        if np.random.random() <= self.learning_p:
            for route in self.routes_costs_somatories.keys():
                v1 = (1.0/(self.routes_costs_somatories[route]+epsilon))
                v2 = 0.0
                for route2 in self.routes_costs_somatories.keys():
                    v2 += (1.0/(self.routes_costs_somatories[route2]+epsilon))
                p = v1/v2
                self.p_table[route] = ((self.delta)*p) + ((1-self.delta)*self.p_table[route])

    def update_agent(self,route,new_cost):
        r = route_to_string(route)
        #self.routes_costs[r].append(new_cost)
        self.routes_costs_somatories[r]+=new_cost
        self.routes_usage[r] += 1
        self.update_p_table()

    def select_route(self):
        routes = []
        prob = []
        for route in self.p_table.keys():
            routes.append(route)
            prob.append(self.p_table[route])
        r = np.random.choice(routes,p=prob)
        #print r + " (p=" + str(self.p_table[r]) + ")"
        return string_to_route(r)

    def select_route_except(self,exception):
        routes = []
        prob = []
        n_routes = len(self.p_table.keys())-1
        except_p = self.p_table[exception]
        for route in self.p_table.keys():
            if route != exception:
                routes.append(route)
                prob.append(self.p_table[route] + (except_p/n_routes))
        r = np.random.choice(routes,p=prob)
        #print r + " (p=" + str(self.p_table[r]) + ")"
        return string_to_route(r)

    def process_forecast(self,route,cost):
        if self.forecast:
            if not(self.resistence):
                self.update_agent(route,cost)
                r = route_to_string(route)
                mean = (self.routes_costs_somatories[r]+epsilon)/(self.routes_usage[r] + epsilon)
                if cost <= mean:
                    return route
                else: #choose another route
                    return self.select_route_except(r)
            else: #resistent to forecast
                r = route_to_string(route)
                mean = (self.routes_costs_somatories[r]+epsilon)/(self.routes_usage[r] + epsilon)
                if np.random.random() <= fermi_mistrust(mean,cost,fermiK):
                    self.update_agent(route,cost)
                    #print(r,mean,cost)
                    return route
                else:
                    return self.select_route_except(r)                    
        else:
            return route



