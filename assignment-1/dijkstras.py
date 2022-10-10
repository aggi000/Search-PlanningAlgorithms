import heapq
import random
from search import algorithms



def dijkstra(s_initial, s_goal, graph):
    open_heap = []
    closed_hash = {}
    heapq.heappush(open_heap,s_initial)
    closed_hash[state_hash(s_initial)] =  s_initial
    expanisons = 0
    while (len(open_heap)!=0):
        n = heapq.heappop(open_heap)
        if(n==s_goal):
            return open_heap.pop(), getg(), expanisons
        nodes = graph.successors(n)
        for node in nodes:
            hash_key = node.state_hash
            if(hash_key not in closed_hash):
                node.set_g(n.get_g() + graph.cost(n.get_x() - node.get_y, n.get_y() - node.get_y()))
                heapq.heappush(open_heap,node)
                closed_hash[hash_key] = node
            node_m = node.get_g()
        if(hash_key in closed_hash and node_m<closed_hash[hash_key].get_g()):
            open_heap[open_heap.index(node)].set_g(node_m)
            closed_hash[graph.successors(n).index(node)] = node
    return open_heap.pop.get_g(),expanisons




