import unittest

from direct_graph import DirectGraph
from undirect_graph import UndirectGraph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.G1 = DirectGraph([['a','b'],['a','c'],['b','e'],['c','b'], \
                               ['c','d'],['c','f'],['d','b'],['d','e'], \
                               ['d','g'],['e','g'],['f','d'],['f','g']], \
                               [8,5,18,10,3,16,2,12,14,4,30,26])
        self.result = [[0,8,5,20,8,21,22]]

        self.G2 = DirectGraph([['b','a'],['b','c'],['a','d'],['c','f'], \
                               ['d','e'],['d','h'],['e','g']], \
                               [8,5,18,10,3,16,2])

        self.UG = UndirectGraph([['a','b'],['a','c'],['b','c'],['b','d'], \
                                 ['c','e'],['b','e'],['d','e']], \
                                 [1,7,5,4,6,3,2])

    def test_bellman_ford(self):
        result = [self.G1.bellman_ford('a')]
        self.assertTrue(DirectGraph.compare_rows(self.result,result,0,0))

    def test_dijkstra(self):
        result = [self.G1.dijkstra('a')]
        self.assertTrue(DirectGraph.compare_rows(self.result,result,0,0))

    def test_floyd_warshall(self):
        result_bellman = []
        for node in ['a','b','c','e','d','f','g']:
            result_bellman.append(self.G1.bellman_ford(node))
        result_floyd = self.G1.floyd_warshall()

        check = True
        for i in range(len(result_bellman)):
            if not DirectGraph.compare_rows(result_bellman,result_floyd,i,i):
                check = False
                break

        self.assertTrue(check)

    def test_topological_sort1(self):
        self.assertTrue(len(self.G1.topological_sort()) == 0)

    def test_topological_sort2(self):
        self.assertTrue(self.G2.topological_sort() == ['f', 'c', 'h', 'g', 'e', \
                                                       'd', 'a', 'b'])

    def test_mst(self):
        self.assertTrue(self.UG.prim()[1] == self.UG.kruskal()[1] == 11)

if __name__ == '__main__':
    unittest.main()
