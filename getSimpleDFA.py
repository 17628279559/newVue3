# -*- coding:utf-8 -*-
import re
from graphviz import Digraph
import time
import os
from copy import deepcopy
os.environ["PATH"] += os.pathsep + r'C:/Program Files/Graphviz/bin/'


class simpleDFAnode(object):
    num = 0

    def __init__(self):
        self.name = simpleDFAnode.num
        simpleDFAnode.num += 1
        self.data = []
        self.node = []
        self.nextnode = {}
        self.needchaifen = True
        self.is_terminator = False
        self.is_beginnode = False


class DFAnode(object):
    num = 0

    def __init__(self):
        self.name = DFAnode.num
        DFAnode.num += 1
        self.data = {}
        self.nextnode = []
        self.is_terminator = False
        self.is_beginnode = False


class node(object):
    num = 0

    def __init__(self, nextnode=[], is_beginnode=False, is_terminator=False):
        self.name = node.num
        node.num += 1
        self.nextnode = nextnode
        self.is_terminator = is_terminator
        self.is_beginnode = is_beginnode


class DFA(object):
    def __init__(self, S=[], alphabet=[], S0=[], Z=[]):
        self.S = S
        self.alphabet = alphabet
        self.S0 = S0
        self.Z = Z

    def NFA_transform_DFA_1(self, nfa):
        start_set = []
        all_start_set = nfa.S0[0].nextnode
        stackk = nfa.S0[0].nextnode
        while stackk:
            if stackk[0][1] == "null" and stackk[0][0] not in start_set:
                start_set.append(stackk[0][0])
                for i in nfa.return_x(stackk[0][0]).nextnode:
                    if i not in all_start_set:
                        all_start_set.append(i)
                        stackk.append(i)
            stackk = stackk[1:]

        set_stack = []

        node1 = DFAnode()
        node1.data = start_set
        node1.is_beginnode = True
        self.S.append(node1)
        self.S0.append(node1)

        set_stack.append(node1)

        while len(set_stack) > 0:
            for i in nfa.alphabet:
                new_set = []
                for nod in set_stack[0].data:  # nod = X,1,2,3
                    nodd = nfa.return_x(nod)
                    for next_node in nodd.nextnode:
                        if next_node[1] == i and next_node[0] not in new_set:
                            new_set.append(next_node[0])
                            self.NFA_transform_DFA_2(
                                new_set, nfa, next_node[0])
                if new_set:
                    self.appendd(i, set_stack, new_set)
            set_stack = set_stack[1:]  # 模拟队列弹出首项

        for i in self.S:
            for j in i.data:
                if j == nfa.Z[0].name:  # 包含结束状态
                    i.is_terminator = True

    def NFA_transform_DFA_2(self, new_set, nfa, next_node):
        next_node = nfa.return_x(next_node)
        for i in next_node.nextnode:
            if i[1] == 'null' and i[0] not in new_set:
                new_set.append(i[0])
                self.NFA_transform_DFA_2(new_set, nfa, i[0])
        return True

    def appendd(self, str, a, b):
        for i in self.S:
            if len(i.data) == len(b):
                j = 0
                while j < len(i.data):
                    if i.data[j] not in b:
                        break
                    else:
                        j += 1
                if j == len(i.data):
                    # 有
                    a[0].nextnode.append([i.name, str])
                    return False
            else:
                continue
        node2 = DFAnode()
        node2.data = b
        a[0].nextnode.append([node2.name, str])
        a.append(node2)
        self.S.append(node2)

        return True


class NFA(object):
    operator = ['(', ')', '|', '*', '+']

    def __init__(self, S=[], alphabet=[], S0=[], Z=[]):
        self.S = S
        self.alphabet = alphabet
        self.S0 = S0
        self.Z = Z

    def normaltype_transform_NFA_1(self, NT):
        str = []
        for i in NT:
            if i not in self.operator:
                str.append(i)
        str = list(set(str))
        self.alphabet = str

        a, b = self.normaltype_transform_NFA_2(NT)
        return a, b

    def return_x(self, x):
        for i in self.S:
            if i.name == x:
                return i

    def normaltype_transform_NFA_2(self, NT):
        b = node([], [])
        a = node([], [])

        self.S.append(a)
        self.S.append(b)

        or_location = []
        for i in range(len(NT)):
            if NT[i] == '|' and self.judge_or_location(NT, i):
                or_location.append(i)

        son_Nt = []
        start_iloc = 0
        for i in range(len(or_location)):
            son_Nt.append(NT[start_iloc:or_location[i]])
            start_iloc = or_location[i]+1
        son_Nt.append(NT[start_iloc:])

        if len(son_Nt) != 1:
            for i in son_Nt:
                start, end = self.normaltype_transform_NFA_3(i)
                a.nextnode.append([start.name, "null"])
                end.nextnode.append([b.name, "null"])
        elif not re.findall(r"\(", son_Nt[0]):
            start, end = self.normaltype_transform_NFA_3(son_Nt[0])
            a.nextnode.append([start.name, "null"])
            end.nextnode.append([b.name, "null"])
        else:
            start, end = self.normaltype_transform_NFA_3(son_Nt[0])
            a.nextnode.append([start.name, "null"])
            end.nextnode.append([b.name, "null"])

        return a, b

    def normaltype_transform_NFA_3(self, NT):

        c = 1
        d = 1

        kuo = []
        son_Nt = []
        i = 0
        start = 0
        while i < len(NT):
            if NT[i] == '(':
                kuo.append('(')
            if NT[i] == ')':
                kuo.pop()
            if len(kuo) == 0:
                if i+1 < len(NT) and NT[i+1] == '*':
                    son_Nt.append(NT[start:i+2])
                    start = i+2
                    i += 2
                    continue
                else:
                    son_Nt.append(NT[start:i+1])
                    start = i+1
                    i += 1
                    continue
            i += 1
        for s_nt in son_Nt:
            if s_nt[0] != '(':
                if s_nt[-1] == '*':
                    start, end = self.normaltype_transform_NFA_4(s_nt[:-1])
                    if d != 1:
                        d.nextnode.append([start.name, "null"])
                    start.nextnode.append([end.name, "null"])
                    end.nextnode.append([start.name, "null"])
                    if c == 1:
                        c = start
                    d = end
                else:
                    start, end = self.normaltype_transform_NFA_4(s_nt)
                    if d != 1:
                        d.nextnode.append([start.name, "null"])
                    if c == 1:
                        c = start
                    d = end
            if s_nt[0] == '(':
                if s_nt[-1] == '*':
                    start, end = self.normaltype_transform_NFA_2(s_nt[1:-2])
                    if d != 1:
                        d.nextnode.append([start.name, "null"])
                    start.nextnode.append([end.name, "null"])
                    end.nextnode.append([start.name, "null"])
                    if c == 1:
                        c = start
                    d = end
                else:
                    start, end = self.normaltype_transform_NFA_2(s_nt[1:-1])
                    if d != 1:
                        d.nextnode.append([start.name, "null"])
                    if c == 1:
                        c = start
                    d = end

        return c, d

    def normaltype_transform_NFA_4(self, NT):
        e = node([], [])
        f = node(nextnode=[[e.name, NT[0]]])
        self.S.append(f)
        self.S.append(e)

        return f, e

    def judge_or_location(self, NT, x):
        left_kuo = 0
        reght_kuo = 0
        for i in range(x):
            if NT[i] == '(':
                left_kuo += 1
            if NT[i] == ')':
                reght_kuo += 1
        if left_kuo == reght_kuo:
            return True
        else:
            return False


def keyinonenoed(nodelist, a, b):
    for i in nodelist:
        if a in i.data and b in i.data:
            return True
    return False


def judge2(newitem, nodelist):
    nextnode = newitem.node[0].nextnode
    if not nextnode:
        for item in newitem.node:
            if item.nextnode:
                return False
    else:
        for item in newitem.node[1:]:
            if len(item.nextnode) != len(nextnode):
                return False
            for key in nextnode:
                if key not in item.nextnode:
                    return False
                if not keyinonenoed(
                        nodelist, nextnode[key], item.nextnode[key]):
                    return False
    return True


def judge_is_over(nodelist):
    ll = 0
    for newitem in nodelist:
        if judge2(newitem, nodelist):
            ll += 1
    if ll == len(nodelist):
        return True
    else:
        return False


def chaifen(nodelist):
    tmp = []
    for newitem in nodelist:
        removetmp = []
        if len(newitem.node) == 1:
            continue
        if not judge2(newitem, nodelist):
            first_node = newitem.node[0]
            newsnode = simpleDFAnode()
            newsnode.data.append(first_node.name)
            newsnode.node.append(first_node)
            removetmp.append(first_node)
            for node in newitem.node:
                lenn = 0
                if len(node.nextnode) != len(first_node.nextnode):
                    continue
                for key in node.nextnode:
                    if key not in first_node.nextnode:
                        break
                    if not keyinonenoed(
                            nodelist, node.nextnode[key], first_node.nextnode[key]):
                        break
                    lenn += 1
                if lenn == len(node.nextnode) and node.name != first_node.name:
                    newsnode.data.append(node.name)
                    newsnode.node.append(node)
                    removetmp.append(node)
            tmp.append(newsnode)
        for rem in removetmp:
            newitem.data.remove(rem.name)
            newitem.node.remove(rem)
        if removetmp:  # 神来之笔
            break
    nodelist.extend(tmp)


def DFA_to_simpleDFA(S):
    start = simpleDFAnode()
    end = simpleDFAnode()
    nodelist = []
    for i in S:
        if i.is_terminator:
            end.data.append(i.name)
            end.node.append(i)
        else:
            start.data.append(i.name)
            start.node.append(i)
    if len(start.data) != 0:
        nodelist.append(start)
        nodelist.append(end)
    else:
        nodelist.append(end)
    while not judge_is_over(nodelist):
        chaifen(nodelist)
    return nodelist


def returnsdfa(nodelist, index):
    for i in nodelist:
        if index in i.data:
            return i.name


def normaltype_to_NFA_to_DFA_to_simpleDFA(normaltype):
    a = NFA()
    start, end = a.normaltype_transform_NFA_1(normaltype)
    start.is_beginnode = True
    end.is_terminator = True
    a.S0.append(start)
    a.Z.append(end)
    b = DFA()
    b.NFA_transform_DFA_1(a)
    b.alphabet = a.alphabet

    for item in b.S:
        tmp = {}
        for i in item.nextnode:
            tmp[i[1]] = i[0]
        item.nextnode = tmp

    nodelist = DFA_to_simpleDFA(b.S)
    for node in nodelist:
        for i in node.node[0].nextnode:
            node.nextnode[i] = returnsdfa(nodelist, node.node[0].nextnode[i])

    for i in nodelist:
        for j in i.node:
            if j.is_terminator:
                i.is_terminator = True
            if j.is_beginnode:
                i.is_beginnode = True
    graph = Digraph(name="newpic", format="png")
    starttt = -1
    for i in nodelist:
        if i.is_beginnode:
            starttt = i.name
        if i.is_terminator:
            graph.attr(rankdir='LR')
            graph.attr('node', shape='doublecircle')
            graph.node(str(i.name))
            continue

        graph.attr('node', shape='circle')
        graph.node(str(i.name))

    for i in nodelist:
        for j in i.nextnode:
            graph.edge(str(i.name), str(i.nextnode[j]), j)
    graph.attr('node', shape='plaintext')
    graph.edge('', str(starttt))
    pic_name = str(time.time())+'_dfa'
    graph.render('vue/pythonImg/'+pic_name, view=False)
    result = {'name': "/pythonImg/"+pic_name+'.png'}
    return result


# normaltype_to_NFA_to_DFA_to_simpleDFA("(a|b)|(c|d)*")
