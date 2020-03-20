import unittest

from graph import Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.G = Graph([['a','b'],['a','c'],['b','e'],['c','b'], \
                        ['c','d'],['c','f'],['d','b'],['d','e'], \
                        ['d','g'],['e','g'],['f','d'],['f','g']], \
                        [8,5,18,10,3,16,2,12,14,4,30,26])
        self.result = [[0,8,5,20,8,21,22]]

    def test_bellman_ford(self):
        result = [self.G.bellman_ford('a')]
        self.assertTrue(Graph.compare_rows(self.result,result,0,0))

    def test_dijkstra(self):
        result = [self.G.dijkstra('a')]
        self.assertTrue(Graph.compare_rows(self.result,result,0,0))

    def test_floyd_warshall(self):
        result_bellman = []
        for node in ['a','b','c','e','d','f','g']:
            result_bellman.append(self.G.bellman_ford(node))
        result_floyd = self.G.floyd_warshall()
        
        check = True
        for i in range(len(result_bellman)):
            if not Graph.compare_rows(result_bellman,result_floyd,i,i):
                check = False
                break

        self.assertTrue(check)

if __name__ == '__main__':
    unittest.main()
