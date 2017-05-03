KSP v1.42

DESCRIPTION
Compute the K shortest loopless paths between two nodes of a given graph, using Yen's algorithm [1]. Complete instructions available at [2].

USAGE
python KSP.py [-h] -f FILE -k K [-l OD_LIST] [-n FLOW]

Or:

./KSP.py [-h] -f FILE -k K [-l OD_LIST] [-n FLOW]

	-h, --help	show this help message and exit
	-f FILE		the graph file
	-k K		number of shortest paths to find
	-l OD_LIST  list of OD-pairs, in the format 'O|D;O|D;[and so on]', where O are valid origin nodes, and D are valid destination nodes
	-n FLOW      number of vehicles (flow) to consider when computing the links' costs


GRAPH FILE FORMATTING INSTRUCTIONS
See [3] for complete instructions.

REFERENCES
[1] Yen, J.Y.: Finding the k shortest loopless paths in a network. Management Science 17(11) (1971) 712-716.
[2] http://wiki.inf.ufrgs.br/K_Shortest_Loopless_Paths.
[3] http://wiki.inf.ufrgs.br/network_files_specification.

AUTHOR
Created in February 10, 2014, by Gabriel de Oliveira Ramos <goramos@inf.ufrgs.br>.
