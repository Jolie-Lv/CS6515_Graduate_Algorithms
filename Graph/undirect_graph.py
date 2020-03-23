import heapq
import sets

class UndirectGraph(object):
    def __init__(self, G, w):
        """
            arg:
                G = undirectional graph, containing lists of edges
                w = weight for each edges
        """
        self.weights = {} # {start: {dest1: w1, dest2: w2, ...}, ...}
        self.labels = {}
        self.edges = []
        self.__prepare_graph(G, w)

    def __prepare_graph(self, G, w):
        """
            1.convert node label to number of 0-based: self.labels
            2.collect edges info: self.weights
        """
        ni = 0
        for i in range(len(G)):
            for node in G[i]:
                if self.labels.get(node) is None:
                    self.labels[node] = ni
                    ni += 1

                if self.weights.get(self.labels[node]) is None:
                    self.weights[self.labels[node]] = {}

            n1 = self.labels[G[i][0]]
            n2 = self.labels[G[i][1]]
            self.edges.append([n1,n2])
            self.weights[n1][n2] = w[i]
            self.weights[n2][n1] = w[i]

    def prim(self):
        queue = [[0,0,0]]
        is_visited = [False]*len(self.labels)

        ret = [[0 for i in range(len(self.labels))] for j in range(len(self.labels))]
        min_dist = 0

        while len(queue) > 0:
            dist, start, dest = heapq.heappop(queue)
            if not is_visited[dest]:
                ret[start][dest] = dist
                ret[dest][start] = dist
                is_visited[dest] = True
                min_dist += dist

                for node in self.weights[dest]:
                    if not is_visited[node]:
                        heapq.heappush(queue, [self.weights[dest][node], dest, node])

        return ret, min_dist

    def kruskal(self):
        edges = [[self.weights[n1][n2],n1,n2] for n1,n2 in self.edges]
        edges.sort()

        node2grp = [-1]*len(self.labels)
        grp2nodes = {}

        ret = [[0 for i in range(len(self.labels))] for j in range(len(self.labels))]
        min_dist = 0

        for w, n1, n2 in edges:
            ret[n1][n2] = ret[n2][n1] = self.weights[n1][n2]
            min_dist += self.weights[n1][n2]
            if node2grp[n1] == -1 and node2grp[n2] == -1:
                node2grp[n1] = n1
                node2grp[n2] = n1
                grp2nodes[n1] = sets.Set()
                grp2nodes[n1].add(n1)
                grp2nodes[n1].add(n2)
            elif node2grp[n1] == -1:
                node2grp[n1] = node2grp[n2]
                grp2nodes[node2grp[n1]].add(n1)
            elif node2grp[n2] == -1:
                node2grp[n2] = node2grp[n1]
                grp2nodes[node2grp[n2]].add(n2)
            elif node2grp[n1] != node2grp[n2]:
                biggrpn1 = node2grp[n1]
                biggrpn2 = node2grp[n2]
                for n in grp2nodes[biggrpn2]:
                    grp2nodes[biggrpn1].add(n)
                    node2grp[n] = biggrpn1
                del grp2nodes[biggrpn2]
            else:
                ret[n1][n2] = ret[n2][n1] = 0
                min_dist -= self.weights[n1][n2]

        return ret, min_dist
