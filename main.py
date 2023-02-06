import copy
from regex import *
from state import * 
from nfa import *
from dfa import *

# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    dfa = DFA()
    for a in nfa.alphabet:
        dfa.alphabet.append(a)
    visited = {}
    dq = deque()
    nset = nfa.epsilonClose_modified({nfa.states[0]})
    visited[0] = nset
    dfa.states.append(State(0))
    dfa.is_accepting[0] = False
    dq.append(nset)
    while len(dq) != 0:
        ss = dq.pop()    
        kid = -1  
        for key in visited:
            if visited[key] == ss:
                kid = key
        for a in dfa.alphabet:
            mes = set()
            for s in ss:
                if nfa.is_accepting[s.id] == True:
                    dfa.is_accepting[kid] = True
                if a in s.transition:
                    for ns in s.transition[a]:
                        mes.add(ns)
            mest = nfa.epsilonClose_modified(mes)
            found = False
            for key in visited:
                if mest == visited[key]:
                    dfa.addTransition(dfa.states[kid],dfa.states[key],a)
                    found = True
                    break
            if not found:
                i = len(dfa.states)
                visited[i] = mest
                dfa.states.append(State(i))
                dfa.is_accepting[i] = False
                dfa.addTransition(dfa.states[kid],dfa.states[i],a)
                dq.append(mest)
    return dfa

# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa = NFA()
    for ds in dfa.states:
        nfa.states.append(State(ds.id))
        nfa.is_accepting[ds.id] = dfa.is_accepting[ds.id]
    for ds in dfa.states:
        for key in ds.transition:
            for n in ds.transition[key]:
                nfa.addTransition(nfa.states[ds.id],nfa.states[n.id],key)
    for a in dfa.alphabet:
        nfa.alphabet.append(a)
    return nfa
# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1 = re1.transformToNFA()
    nfa2 = re2.transformToNFA()
    dfa1 = nfaToDFA(nfa1)
    dfa2 = nfaToDFA(nfa2)
    cdfa1 = dfa1.complement()
    cdfa2 = dfa2.complement()
    bnfa1 = dfaToNFA(cdfa1)
    bnfa2 = dfaToNFA(cdfa2)
    #-----------------------------#
    res1 = bnfa1.union(nfa2)
    res2 = nfa1.union(bnfa2)
    dres1 = nfaToDFA(res1)
    dres2 = nfaToDFA(res2)
    ans1 = dres1.complement()
    ans2 = dres2.complement()
    str1 = ans1.shortestString()
    str2 = ans2.shortestString()
    #print(str1)
    #print(str2)
    if str1 == None and str2 == None:
        return True
    else:
        return False

if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(nfa, s, expected):
        # test your dfa conversion
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print("The DFA gave ",res, " as expected on ", s)
        else:
            print("**** ", "The DFA gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass

    #tests written by students
    '''
    re = parse_re("((ab|cd)*|(de*fg|h(ij)*klm*n|q))*")
    nfa = re.transformToNFA()
    print("--nfa--")
    for ns in nfa.states:
        for key in ns.transition:
            for s in ns.transition[key]:
                print(nfa.is_accepting[ns.id],':',ns.id,'->',key,'->',s.id, ':', nfa.is_accepting[s.id])
    print(nfa.isStringInLanguage('l'))
    print("--dfa--")
    dfa = nfaToDFA(nfa)
    for ds in dfa.states:
        for key in ds.transition:
            for s in ds.transition[key]:
                print(dfa.is_accepting[ds.id],':',ds.id,'->',key,'->',s.id, ':', dfa.is_accepting[s.id])
    print(dfa.isStringInLanguage('bbcc'))
    print(dfa.shortestString())
    print("--dfa back to nfa--")
    bnfa = dfaToNFA(dfa)
    for bds in bnfa.states:
        for key in bds.transition:
            for cs in bds.transition[key]:
                print(bnfa.is_accepting[bds.id],':',bds.id,'->',key,'->',cs.id, ':', bnfa.is_accepting[cs.id])
    print(bnfa.isStringInLanguage('aabccc'))
    print("--complement dfa--")
    cdfa = dfa.complement()
    for cds in cdfa.states:
        for key in cds.transition:
            for cs in cds.transition[key]:
                print(cdfa.is_accepting[cds.id],':',cds.id,'->',key,'->',cs.id, ':', cdfa.is_accepting[cs.id])
    print(cdfa.isStringInLanguage('ac'))
    '''
    #testEquivalence('ababab', '(ab)*', False)
    #test your NFA:
    #The isStringInLanguage of NFA may cause system to enter an infinite loop
    #testNFA('&', '', True)
    #testNFA('a', '', False)
    #testNFA('a', 'a', True)
    #testNFA('a', 'ab', False)
    #testNFA('a*', '', True)
    #testNFA('a*', 'a', True)
    #testNFA('a*', 'aaa', True)
    #testNFA('a|b', '', False)
    #testNFA('a|b', 'a', True)
    #testNFA('a|b', 'b', True)
    #testNFA('a|b', 'ab', False)
    #testNFA('ab|cd', '', False)
    #testNFA('ab|cd', 'ab', True)
    #testNFA('ab|cd', 'cd', True)
    #testNFA('ab|cd*', '', False)
    #testNFA('ab|cd*', 'c', True)
    #testNFA('ab|cd*', 'cd', True)
    #testNFA('ab|cd*', 'cddddddd', True)
    #testNFA('ab|cd*', 'ab', True)
    #testNFA('((ab)|(cd))*', '', True)
    #testNFA('((ab)|(cd))*', 'ab', True)
    #testNFA('((ab)|(cd))*', 'cd', True)
    #testNFA('((ab)|(cd))*', 'abab', True)
    #testNFA('((ab)|(cd))*', 'abcd', True)
    #testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    #testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    pass
    
