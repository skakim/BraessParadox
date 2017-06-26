from kspmaster import KSP
from Agent import Agent
import sys
import random

# parameters to be passed to the KSP algorithm
graph_file = './network-files-master/Braess-graphs/OQPD.net'    # the graph of the traffic network (the file format is specified by the algorithm's help)
ODpairs = ['O|D'] # the list of origins and destinations
flow = 1.0               # the flow of vehicles to be used when computing the links' costs (the default is zero)("initial optimism" technique of Q-learning)
num_agents = 1500       # the number of agents of the simulation
K = 100                  	# the number of paths to find 
num_iterations = 200    # the number of iterations of the simulation
forecast = True        #forecast given
manipulation = True   #forecast manipulation
invasion = False		#new greedy_agents at num_iterations/3
invasion_proportion = 0.001	#proportion of new greedy_agents
forecast_mistrust = True     #resistance to the forecast

# generate the list of vertices and edges from the network file
V, E, OD, EF = KSP.generateGraph(graph_file, flow)
#print graph_file
#print EF

# for each OD pair
for od in ODpairs: # to look at all pairs, use the variable OD (above)

    #print '-----Pair %s-----' % od
    origin, destination = od.split('|')

    # run the algorithm (return the K routes and associated costs of the given origin-destination pair)
    routes = KSP.getKRoutes(V, E, origin, destination, K)
    #print routes

    p_routes = [str(x[0]) for x in routes]
    #print p_routes
    #print ",".join(map(str,p_routes))
    max_route = max(p_routes, key=len)
    #print max_route
    agents = []

    for i in xrange(num_agents):
        a = Agent(routes,delta=0.8,learning_p=0.2,resistence=forecast_mistrust)
        agents.append(a)
        #if i == 0:
            #print a.p_table

    for it in xrange(num_iterations):
        edges_use = {}
        routes_use = {x:0 for x in p_routes}
        rs = []
	
	    #each agent select his route
        for agent in agents:
            route = agent.select_route()
            routes_use[str(route)] += 1
            #if agent == agents[0]:
                #print p_routes.index(route)
            rs.append(route)
            for edge in route:
                if edge not in edges_use.keys():
                    edges_use[edge] = 1
                else:
                    edges_use[edge] += 1
        usages = []
        #for p in p_routes:
            #usages.append(str(routes_use[p]))
        #print ",".join(usages)
        #print str(routes_use[max_route]),

	    #process edges cost
        costs = {}
        for edge in edges_use.keys():
            EF[edge][0]['f'] = edges_use[edge]
            costs[edge] = EF[edge][1].evaluate(EF[edge][0])
        #print costs

        if not(forecast):
            #update agents
            global_cost = 0.0
            for ai in xrange(len(agents)):
                ag = agents[ai]            
                r = rs[ai]
                cost = 0.0
                for edge in r:
                    #if ai == 0:
                    #print edge,costs[edge]
                    cost += costs[edge]
                #if ai == 0:
                    #print cost
                    #print ag.p_table
                ag.update_agent(r,cost)
                #global_cost += cost
            for route in routes:
                #print route[0]
                cost = 0
                for edge in route[0]:
                    if edge in edges_use.keys():
                        cost += costs[edge]
                global_cost += cost
            #print global_cost#, routes_use[max_route]
            print routes_use[max_route]
        
        else:
            #return forecast and receive new choices
            new_edges_use = {}
            new_routes_use = {x:0 for x in p_routes}
            new_rs = []
            changes = 0
            max_routes_manip = 0
            for ai in xrange(len(agents)):
                ag = agents[ai]
                r = rs[ai]
                cost = 0.0
                for edge in r:
                    cost += costs[edge]
                if manipulation: #information manipulation
                    if str(r) == max_route: #using "shortcut"
                        cost = 99999 #fake info, to make not use this route
                        max_routes_manip += 1
                    else: #not using shortcut
                        cost = 0 #fake info, to make continue using
                #if ai == 0: 
                    #print r,cost,
                route = agent.process_forecast(r,cost)
                new_routes_use[str(route)] += 1
                if route != r:
                    changes += 1
                new_rs.append(route)
                for edge in route:
                    if edge not in new_edges_use.keys():
                        new_edges_use[edge] = 1
                    else:
                        new_edges_use[edge] += 1

		    #process new edges cost
            new_costs = {}
            for edge in new_edges_use.keys():
                EF[edge][0]['f'] = new_edges_use[edge]
                new_costs[edge] = EF[edge][1].evaluate(EF[edge][0])

            #print new_edges_use,new_costs
	
	        #update agents
            global_cost = 0.0
            for ai in xrange(len(agents)):
                ag = agents[ai]            
                r = new_rs[ai]
                cost = 0.0
                for edge in r:
                    #if ai == 0:
                        #print edge,costs[edge]
                    cost += new_costs[edge]
                #if ai == 0:
                    #print cost,
                    #print ag.p_table
                    #print ag.routes_costs_somatories['o->q->p->d']/(ag.routes_usage['o->q->p->d']+(1.0/sys.maxint)),
                    #print ag.routes_costs_somatories['o->q->d']/(ag.routes_usage['o->q->d']+(1.0/sys.maxint)),
                    #print ag.routes_costs_somatories['o->p->d']/(ag.routes_usage['o->p->d']+(1.0/sys.maxint)),
                    #print r,cost,
                ag.update_agent(r,cost)
                #global_cost += cost
            for route in routes:
                #print route[0]
                cost = 0
                for edge in route[0]:
                    if edge in new_edges_use.keys():
                        cost += new_costs[edge]
                global_cost += cost
            #print global_cost#new_routes_use[max_route]
            print new_routes_use[max_route]
        
        if invasion and (it == num_iterations/3):
            #print("INVASION!")
            n_stay = int(num_agents*(1.0-invasion_proportion))
            n_leave = int(num_agents-n_stay)
            agents = random.sample(agents, n_stay)
            for _ in xrange(n_leave):
                a = Agent(routes,delta=0.8,learning_p=0.2,forecast=False) #new agents that doesn't receive forecast
                agents.append(a)
            





