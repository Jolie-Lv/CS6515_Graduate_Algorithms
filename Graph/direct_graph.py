import heapq
import copy
import sets

class DirectGraph(object):
    def __init__(self, G, w):
        """
            arg:
                G = directional graph, containing lists of edges
                w = weight for each edges
        """
        self.weights = {} # {start: {dest1: w1, dest2: w2, ...}, ...}
        self.reversed_edges = {} # {dest: [start1, start2, ...], ...}
        self.labels = {}
        self.labels_num = []
        self.__prepare_graph(G, w)

    def __prepare_graph(self, G, w):
        """
            1.convert node label to number of 0-based: self.labels
            2.collect edges info: self.weights, self.reversed_edges
        """
        for i in range(len(G)):
            # keep map from actual node to 0-based num node
            for node in G[i]:
                if self.labels.get(node) is None:
                    self.labels[node] = len(self.labels_num)
                    self.labels_num.append(node)

            start = self.labels[G[i][0]]
            dest = self.labels[G[i][1]]

            # collect edges with weights
            if self.weights.get(start) is None:
                self.weights[start] = {}
            self.weights[start][dest] = w[i]

            # construct map from dest node to adj nodes
            if self.reversed_edges.get(dest) is None:
                self.reversed_edges[dest] = []
            self.reversed_edges[dest].append(start)

    # Dynamic Programming
    def bellman_ford(self, s):
        """
            arg:
                s = start node
            return:
                min distance from s to other nodes
        """
        n = len(self.labels)
        DP = [[float('inf') for j in range(n)] for i in range(n+1)]
        DP[0][self.labels[s]] = 0

        for i in range(1, n+1):
            for j in range(n):
                DP[i][j] = DP[i-1][j]
                if self.reversed_edges.get(j) is not None:
                    for adj in self.reversed_edges[j]:
                        DP[i][j] = min(DP[i][j], DP[i-1][adj]+self.weights[adj][j])
            if DirectGraph.compare_rows(DP, DP, i-1, i):
                return DP[i]

        if not DirectGraph.compare_rows(DP, DP, n, n-1):
            assert "There are negative weights in graph"
        return DP[-1]

    def dijkstra(self, s):
        ret = [None]*len(self.labels)

        priorityq = []
        heapq.heappush(priorityq, [0, self.labels[s]])

        while len(priorityq) > 0:
            dist, node = heapq.heappop(priorityq)
            if ret[node] is None:
                ret[node] = dist
            if self.weights.get(node) is not None:
                for adj in self.weights[node]:
                    new_dist = dist+self.weights[node][adj]
                    heapq.heappush(priorityq, [new_dist, adj])

        return ret

    def floyd_warshall(self):
        n = len(self.labels)
        DP = [[[float('inf') for k in range(n)] for j in range(n)] for i in range(n+1)]

        for start in self.weights:
            for dest in self.weights[start]:
                DP[0][start][dest] = self.weights[start][dest]

        for node in range(n):
            DP[0][node][node] = 0

        for i in range(1, n+1):
            for j in range(n):
                for k in range(n):
                    DP[i][j][k] = min(DP[i-1][j][k], DP[i-1][j][i-1]+DP[i-1][i-1][k])

        return DP[-1]

    # max flow
    def ford_fulkerson(self, s, t):
        s = self.labels[s]
        t = self.labels[t]
        residual = {}
        for node in self.weights:
            residual[node] = {}
            for dest in self.weights[node]:
                residual[node][dest] = 0

        return self.__ford_fulkerson_impl(s, t, residual)

    def __ford_fulkerson_impl(self, s, t, residual):
        is_visited = [False]*len(self.labels)
        stack = [s]
        while len(stack) > 0:
            node = stack[-1]
            if node == t:
                path = [node]
                while len(stack) > 0:
                    n = stack.pop()
                    if is_visited[n]:
                        path.append(n)

                """
                    find minimum flow
                """
                flow = float('inf')
                for i in range(1,len(path)):
                    start = path[i]
                    dest = path[i-1]
                    if self.weights.get(start) is not None and \
                       self.weights[start].get(dest) is not None:
                       flow = min(flow, self.weights[start][dest] - \
                                        residual[start][dest])
                    else:
                        flow = min(flow, residual[dest][start])

                """
                    update residual graph
                """
                for i in range(1,len(path)):
                    start = path[i]
                    dest = path[i-1]
                    if self.weights.get(start) is not None and \
                       self.weights[start].get(dest) is not None:
                       residual[start][dest] += flow
                    else:
                        residual[dest][start] -= flow

                return flow + self.__ford_fulkerson_impl(s, t, residual)

            elif is_visited[node]:
                is_visited[node] = False
                stack.pop()
                continue

            else:
                is_visited[node] = True
                if self.weights.get(node) is not None:
                    for dest in self.weights[node]:
                        if not is_visited[dest] and \
                           residual[node][dest] < self.weights[node][dest]:
                           stack.append(dest)
                if node != s and len(self.reversed_edges[node]) > 0:
                    for dest in self.reversed_edges[node]:
                        if not is_visited[dest] and \
                           residual[dest][node] > 0:
                           stack.append(dest)

        return 0

    def topological_sort(self):
        is_dag, post = self.__is_dag()
        ret = [-1]*len(self.labels)
        for node in self.labels:
            ret[post[self.labels[node]]] = node
        return ret, is_dag

    def strongly_connected_components(self):
        reversed_graph = copy.deepcopy(self)
        reversed_graph.__reversed_graph()
        sort_r, _ = reversed_graph.topological_sort()

        ret = []
        is_visited = sets.Set()
        stack = []

        for i in range(1,len(sort_r)+1):
            sink = sort_r[-i]
            if sink not in is_visited:
                ret.append([])
                stack.append(sink)
                while len(stack) > 0:
                    node = stack.pop()
                    if node not in is_visited:
                        ret[-1].append(node)
                        is_visited.add(node)
                        if self.weights.get(self.labels[node]) is not None:
                            for dest in self.weights[self.labels[node]]:
                                if self.labels_num[dest] not in is_visited:
                                    stack.append(self.labels_num[dest])

        return ret

    def __is_dag(self):
        is_visited = {}
        count = 0
        for root in range(len(self.labels)):
            if is_visited.get(root) is None:
                stack = [root]
                is_visited[root] = -2
                while len(stack) > 0:
                    node = stack[-1]
                    if is_visited[node] == -2:
                        is_visited[node] = -1
                        if self.weights.get(node) is not None:
                            for child in self.weights[node]:
                                if is_visited.get(child) is None:
                                    stack.append(child)
                                    is_visited[child] = -2
                    elif is_visited[node] == -1:
                        stack.pop()
                        is_visited[node] = count
                        count += 1

        for node in self.weights:
            for child in self.weights[node]:
                if is_visited[child] > is_visited[node]:
                    return False, is_visited

        return True, is_visited

    def __reversed_graph(self):
        new_weights = {}
        self.reversed_edges = {}

        for start in self.weights:
            self.reversed_edges[start] = []
            for dest in self.weights[start]:
                self.reversed_edges[start].append(dest)
                if new_weights.get(dest) is None:
                    new_weights[dest] = {}
                new_weights[dest][start] = self.weights[start][dest]

        self.weights = new_weights

    @staticmethod
    def compare_rows(array1, array2, row1, row2):
        """
            return:
                true if values of row1 in array1 and row2 in array2 are identical
        """
        if row1 >= len(array1) or row2 >= len(array2) or len(array1[0]) != len(array2[0]):
            return Falses

        for i in range(len(array1[0])):
            if array1[row1][i] != array2[row2][i]:
                return False
        return True
