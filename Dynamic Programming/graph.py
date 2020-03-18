import sets

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
        DP = [[float('inf') for j in range(n)] for i in range(n)]
        DP[0][self.labels[s]] = 0

        for i in range(1, n):
            for j in range(n):
                DP[i][j] = DP[i-1][j]
                if self.reversed_edges.get(j) is not None:
                    for adj in self.reversed_edges[j]:
                        DP[i][j] = min(DP[i][j], DP[i-1][adj]+self.weights[adj][j])
        return DP[-1]

if __name__ == '__main__':
    """test"""
    G = Graph([['a','b'],['b','c']],[1,4])
    print G.bellman_ford('a')
