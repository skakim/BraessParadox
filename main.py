from kspmaster import KSP
from Agent import Agent

# parameters to be passed to the KSP algorithm
graph_file = './network-files-master/Braess-graphs/Braess_5_4200_10_c1.net'    # the graph of the traffic network (the file format is specified by the algorithm's help)
ODpairs = ['s|t'] # the list of origins and destinations
K = 1000                  	# the number of paths to find
flow = 0.0               # the flow of vehicles to be used when computing the links' costs (the default is zero)

# generate the list of vertices and edges from the network file
V, E, OD = KSP.generateGraph(graph_file, flow)
print graph_file

# for each OD pair
for od in ODpairs: # to look at all pairs, use the variable OD (above)

    #print '-----Pair %s-----' % od
    origin, destination = od.split('|')

    # run the algorithm (return the K routes and associated costs of the given origin-destination pair)
    routes = KSP.getKRoutes(V, E, origin, destination, K)

    for i in xrange(1000):
        a = Agent(routes)
        a.select_route()
