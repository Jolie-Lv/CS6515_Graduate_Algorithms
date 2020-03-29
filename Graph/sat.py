import sets

from direct_graph import DirectGraph

class CNF(object):
    def __init__(self, cnf):
        self.cnf = CNF.__simplify_cnf(cnf)

    def sat2(self):
        G = CNF.__construct_graph(self.cnf)
        scc = G.strongly_connected_components()
        ret = {}
        for i in range(len(scc)):
            is_sink = (ret.get(scc[i][0] if scc[i][0][0] != '-' else scc[i][0][1:]) is None)
            if is_sink:
                for literal in scc[i]:
                    if literal[0] == '-':
                        if ret.get(literal[1:]) is None:
                            ret[literal[1:]] = False
                        else:
                            return 'provided cnf is not satisfiable'
                    else:
                        if ret.get(literal) is None:
                            ret[literal] = True
                        else:
                            return 'provided cnf is not satisfiable'
            else:
                for literal in scc[i]:
                    if literal[0] == '-':
                        if ret.get(literal[1:]) is None or not ret[literal[1:]]:
                            return 'provided cnf is not satisfiable'
                    else:
                        if ret.get(literal) is None or ret[literal]:
                            return 'provided cnf is not satisfiable'
        return ret

    def value(self, boolean):
        ret = True
        for clause in self.cnf:
            ret = False
            for literal in clause:
                val = (not boolean[literal[1:]]) if literal[0] == '-' \
                                                 else boolean[literal]
                if val:
                    ret = True
                    break
            if not ret:
                break
        return ret

    @staticmethod
    def __simplify_cnf(cnf):
        unit_clause = sets.Set()
        for i in range(len(cnf)):
            if len(cnf[i]) == 1:
                unit_clause.add(cnf[i][0])

        if len(unit_clause) == 0:
            ret = []
            for clause in cnf:
                if len(clause) > 0:
                    ret.append(clause)
            return ret

        for i in range(len(cnf)):
            tmp = []
            for j in range(len(cnf[i])):
                if cnf[i][j] in unit_clause:
                    tmp = []
                    break
                neg_literal = cnf[i][j][1:] if cnf[i][j][0] == '-' else ('-'+cnf[i][j])
                if neg_literal not in unit_clause:
                    tmp.append(cnf[i][j])
            cnf[i] = tmp

        return simplify_cnf(cnf)

    @staticmethod
    def __construct_graph(cnf):
        G = []
        w = []
        for clause in cnf:
            if len(clause) != 2:
                assert 'provided cnf has >2 literals'

            neg_literal0 = clause[0][1:] if clause[0][0] == '-' else ('-'+clause[0])
            neg_literal1 = clause[1][1:] if clause[1][0] == '-' else ('-'+clause[1])
            G.append([neg_literal0,clause[1]])
            G.append([neg_literal1,clause[0]])
            w.append(0) # dummy
            w.append(0) # dummy

        return DirectGraph(G,w)
