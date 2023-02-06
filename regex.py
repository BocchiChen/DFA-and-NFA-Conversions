from nfa import *
from state import *

class Regex:
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans
    def transformToNFA(self):
        pass
    pass

class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        nfa = NFA()
        nfa.states.append(State(0))
        nfa.is_accepting[0] = False
        cnfa1 = self.children[0].transformToNFA()
        cnfa1.is_accepting[len(cnfa1.states)-1] = False
        cnfa2 = self.children[1].transformToNFA()
        cnfa2.is_accepting[len(cnfa2.states)-1] = False
        dic1 = nfa.addStatesFrom(cnfa1)
        dic2 = nfa.addStatesFrom(cnfa2)
        nfa.addTransition(nfa.states[0],nfa.states[dic1[0]])
        nfa.addTransition(nfa.states[dic1[len(cnfa1.states)-1]],nfa.states[dic2[0]])
        i = len(nfa.states)
        nfa.states.append(State(i))
        nfa.is_accepting[i] = True
        nfa.addTransition(nfa.states[dic2[len(cnfa2.states)-1]],nfa.states[i])
        return nfa
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        nfa = NFA()
        nfa.states.append(State(0))
        nfa.is_accepting[0] = False
        nfa2 = self.children[0].transformToNFA()
        nfa2.is_accepting[len(nfa2.states)-1] = False
        nfa2.addTransition(nfa2.states[len(nfa2.states)-1],nfa2.states[0])
        dic = nfa.addStatesFrom(nfa2)
        i = len(nfa.states)
        nfa.states.append(State(i))
        nfa.is_accepting[i] = True
        nfa.addTransition(nfa.states[0],nfa.states[dic[0]])
        nfa.addTransition(nfa.states[0],nfa.states[i])
        nfa.addTransition(nfa.states[dic[len(nfa2.states)-1]],nfa.states[i])
        return nfa
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        nfa = NFA()
        nfa.states.append(State(0))
        nfa.is_accepting[0] = False
        cnfa1 = self.children[0].transformToNFA()
        cnfa1.is_accepting[len(cnfa1.states)-1] = False
        cnfa2 = self.children[1].transformToNFA()
        cnfa2.is_accepting[len(cnfa2.states)-1] = False
        dic1 = nfa.addStatesFrom(cnfa1)
        dic2 = nfa.addStatesFrom(cnfa2)
        nfa.addTransition(nfa.states[0],nfa.states[dic1[0]])
        nfa.addTransition(nfa.states[0],nfa.states[dic2[0]])
        i = len(nfa.states)
        nfa.states.append(State(i))
        nfa.is_accepting[i] = True
        nfa.addTransition(nfa.states[dic1[len(cnfa1.states)-1]],nfa.states[i])
        nfa.addTransition(nfa.states[dic2[len(cnfa2.states)-1]],nfa.states[i])
        return nfa
    pass

class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    def transformToNFA(self):
        nfa = NFA()
        nfa.states.append(State(0))
        nfa.is_accepting[0] = False
        nfa.states.append(State(1))
        nfa.is_accepting[1] = True
        nfa.alphabet.append(self.sym)
        nfa.states[0].transition[self.sym] = {nfa.states[1]}
        return nfa
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    def transformToNFA(self):
        nfa = NFA()
        nfa.states.append(State(0))
        nfa.is_accepting[0] = True
        return nfa
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()