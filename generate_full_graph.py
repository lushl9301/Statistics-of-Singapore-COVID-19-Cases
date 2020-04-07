import networkx as nx
import sys
import re

G = nx.Graph()

def addEdge(a, b):
    """
    add edges between [a1, a2, a3, ...] and [b1, b2, b3, ...]
    :param a:
    :param b:
    """
    for i in a:
        for j in b:
            if i != j:
                G.add_edge(i, j)

def remove_age(s):
    return re.sub("\d+ year-old", "", s)


def remove_date(s):
    mth = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for m in mth:
        element = "\d+ " + m + " 2020"
        t = re.sub(element, " " , s)
        if t:
            s = t
    # s = re.sub("\d+ January 2020", "", s)
    # s = re.sub("\d+ Jan", "", s)
    # s = re.sub("\d+ February 2020", "", s)
    # s = re.sub("\d+ Feb", "", s)
    # s = re.sub("\d+ March 2020", "", s)
    # s = re.sub("\d+ Mar", "", s)
    # s = re.sub("\d+ April 2020", "", s)
    # s = re.sub("\d+ Apr", "", s)
    mth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m in mth:
        element = "\d+ " + m
        t = re.sub(element, " " , s)
        if t:
            s = t
    return s

def remove_time(s):
    mth = ["pm", "am"]
    for m in mth:
        element = "\d+" + m
        t = re.sub(element, " " , s, re.I)
        if t:
            s = t
        element = "\d+" + m
        t = re.sub(element, " " , s, re.I)
        if t:
            s = t
    return s


def analyze_line(s):
    """
    Type 1: [Cc]ase[s] \d+ is\are linked to [Cc]ase[s] \d+
    Type 2: Case \d+ is a \d+ year-old .+ is linked to [Cc]ase
    :param s:
    :return:
    """
    s = s.strip()
    s = remove_age(s)
    s = remove_date(s)
    s = remove_time(s)

    print(s)

    ### case 1 & 2
    x = re.search("[Cc]ase.+linked to.+[cC]ase.+", s)
    if x:
        print("111111111")

def process_file(filename):
    f = open(filename, "r")
    for line in f:
        if "linked to" in line:
            analyze_line(line)

process_file(sys.argv[1])