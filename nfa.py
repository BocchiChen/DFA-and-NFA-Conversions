from state import *
import regex
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass
    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym = '&'):
        if sym not in s1.transition:
            s1.transition[sym] = {s2}
        else:
            s1.transition[sym].add(s2)
        pass
    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        dic = {}
        n = len(self.states)
        for s in nfa.states:
            self.states.append(State(s.id + n))
            self.is_accepting[s.id + n] = nfa.is_accepting[s.id]
            dic[s.id] = s.id + n
        for s in nfa.states:
            for key in s.transition:
                for ts in s.transition[key]:
                    self.addTransition(self.states[dic[s.id]],self.states[dic[ts.id]],key)
        for c in nfa.alphabet:
            if c not in self.alphabet:
                self.alphabet.append(c)
        return dic
    
    def union(self, nfa):
        union_nfa = NFA()
        union_nfa.states.append(State(0))
        union_nfa.is_accepting[0] = False
        self.is_accepting[len(self.states)-1] = False
        nfa.is_accepting[len(nfa.states)-1] = False
        dic1 = union_nfa.addStatesFrom(self)
        dic2 = union_nfa.addStatesFrom(nfa)
        union_nfa.addTransition(union_nfa.states[0],union_nfa.states[dic1[0]])
        union_nfa.addTransition(union_nfa.states[0],union_nfa.states[dic2[0]])
        i = len(union_nfa.states)
        union_nfa.states.append(State(i))
        union_nfa.is_accepting[i] = True
        union_nfa.addTransition(union_nfa.states[dic1[len(self.states)-1]],union_nfa.states[i])
        union_nfa.addTransition(union_nfa.states[dic2[len(nfa.states)-1]],union_nfa.states[i])
        return union_nfa

    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    #on epsilon transitions.
    def epsilonClose(self, ns):
        states = []
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():  
                if sym == '&':
                    for s in nn:
                        states.append(s)
        return states

    def epsilonClose_modified(self, ns):
        res = set()
        q = set()
        for n in ns:
            q.add(n)
        while len(q) != 0:
            node = q.pop()
            if node in res:
                continue
            res.add(node)
            for key in node.transition:
                if key == '&':
                    for n in node.transition[key]:
                        q.add(n)
        return res
    
    # It takes a string and returns True if the string is in the language of this NFA
    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop(0)
            visited.append((currS,pos))
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            if (n,pos) not in visited:
                                queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass
