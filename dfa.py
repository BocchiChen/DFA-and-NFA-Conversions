import copy
from state import *
from queue import deque
import sys

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass  
    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        if sym not in s1.transition:
            s1.transition[sym] = {s2}
        else:
            print("Error!")
        pass
    # You should write this function.
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        cdfa = DFA()
        for ds in self.states:
            cdfa.states.append(State(ds.id))
            cdfa.is_accepting[ds.id] = not self.is_accepting[ds.id]
        for ds in self.states:
            for key in ds.transition:
                for n in ds.transition[key]:
                    cdfa.addTransition(cdfa.states[ds.id],cdfa.states[n.id],key)
        return cdfa
    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, string):
        curr = self.startS
        for s in string:
            if s not in self.alphabet:
                return False
            for key in self.states[curr].transition:
                if key == s:
                    for n in self.states[curr].transition[key]:
                        curr = n.id
        return self.is_accepting[curr]
    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        minlen = sys.maxsize
        res = None
        visited = set()
        dq = deque()
        dq.append([self.states[self.startS],""])
        while len(dq) != 0:
            curr = dq.pop()
            if curr[0].id in visited:
                continue
            if self.is_accepting[curr[0].id] is True and len(curr[1])<minlen:
                minlen = len(curr[1])
                res = curr[1]
            visited.add(curr[0].id)
            for ch in curr[0].transition:
                for s in curr[0].transition[ch]:
                    dq.append([s,curr[1]+ch])
        return res
    pass