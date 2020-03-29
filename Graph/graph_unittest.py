import unittest

from direct_graph import DirectGraph
from undirect_graph import UndirectGraph
from sat import CNF

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

        self.G3 = DirectGraph([['a','b'],['b','d'],['b','e'],['e','b'],['b','c'], \
                               ['c','f'],['e','l'],['f','g'],['g','f'],['g','c'], \
                               ['l','i'],['k','l'],['f','i'],['h','j'],['j','h'], \
                               ['h','i'],['j','k'],['i','j']], \
                               [0]*18)

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
        self.assertFalse(self.G1.topological_sort()[1])

    def test_topological_sort2(self):
        self.assertTrue(self.G2.topological_sort()[0] == ['f', 'c', 'h', 'g', \
                                                          'e', 'd', 'a', 'b'])

    def test_scc(self):
        self.assertTrue(self.G3.strongly_connected_components() == \
            [['l', 'i', 'j', 'h', 'k'], ['c', 'f', 'g'], ['d'], ['b', 'e'], ['a']])

    def test_mst(self):
        self.assertTrue(self.UG.prim()[1] == self.UG.kruskal()[1] == 11)

    def test_sat_satisfiable1(self):
        cnf1 = [['-x1','-x2'],['x2','x3'],['-x3','-x1']]
        cnf1 = CNF(cnf1)
        boolean = cnf1.sat2()
        self.assertTrue(cnf1.value(boolean))

    def test_sat_satisfiable2(self):
        cnf2 = [['x1','x2'],['x2','-x1'],['-x1','-x2']]
        cnf2 = CNF(cnf2)
        boolean = cnf2.sat2()
        self.assertTrue(cnf2.value(boolean))

    def test_sat_unsatisfiable(self):
        cnf3 = [['x1','x2'],['x2','-x1'],['x1','-x2'],['-x1','-x2']]
        cnf3 = CNF(cnf3)
        boolean = cnf3.sat2()
        self.assertTrue(boolean == 'provided cnf is not satisfiable')

if __name__ == '__main__':
    unittest.main()
