def bi_bs(s_initial, s_goal, graph):
    global b_num
    openA = [s_initial]
    openB = [s_goal]
    hp.heapify(openA)
    hp.heapify(openB)

    closedA = {}
    closedB = {}
    closedA[s_initial.state_hash()] = s_initial
    closedB[s_goal.state_hash()] = s_goal

    cost = 999999999
    expanded_astar = 0

    while len(openA) != 0 and len(openB) != 0:
        if cost < openA[0].get_g() + openB[0].get_g():
            return cost, expanded_astar
        if  openA[0] < openB[0]:
            n = hp.heappop(openA)
            expanded_astar += 1
            children = graph.successors(n)
            for child in children:
                if child.state_hash() in closedB:
                    cost = min(cost, closedB[child.state_hash()].get_g() + child.get_g())
                if child.state_hash() in closedA and child < closedA[child.state_hash()]:
                    closedA[child.state_hash()].set_g(child.get_g())
                    # parent updation not necessary
                    hp.heapify(openA)
                if child.state_hash() not in closedA:
                    hp.heappush(openA,child)
                    closedA[child.state_hash()] = child
        else:
            n = hp.heappop(openB)
            expanded_astar += 1
            children = graph.successors(n)
            for child in children:
                if child.state_hash() in closedA:
                    cost = min(cost, closedA[child.state_hash()].get_g() + child.get_g())
                if child.state_hash() in closedB and child < closedB[child.state_hash()]:
                    closedB[child.state_hash()].set_g(child.get_g())
                    # parent updation not necessary
                    hp.heapify(openB)
                if child.state_hash() not in closedB:
                    hp.heappush(openB, child)
                    closedB[child.state_hash()] = child
    # graph.plot_map(closedB, s_initial, s_goal, 'solution-maps/bibs/' + str(b_num))
    # b_num += 1
    return -1, expanded_astar