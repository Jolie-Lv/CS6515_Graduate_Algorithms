import heapq

class Graph(object):
    def __init__(self, G, w):
        """
            arg:
                G = directional graph, containing lists of edges
                w = weight for each edges
        """
        self.weights = {} # {start: {dest1: w1, dest2: w2, ...}, ...}
        self.reversed_edges = {} # {dest: [start1, start2, ...], ...}
        self.labels = {}
        self.__prepare_graph(G, w)

    def __prepare_graph(self, G, w):
        """
            1.convert node label to number of 0-based: self.labels
            2.collect edges info: self.weights, self.reversed_edges
        """
        ni = 0
        for i in range(len(G)):
            # keep map from actual node to 0-based num node
            for node in G[i]:
                if self.labels.get(node) is None:
                    self.labels[node] = ni
                    ni += 1

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
            if Graph.compare_rows(DP, DP, i-1, i):
                return DP[i]

        if not Graph.compare_rows(DP, DP, n, n-1):
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
