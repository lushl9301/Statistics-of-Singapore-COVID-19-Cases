import networkx as nx
import sys
from common import *

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
    s = remove_covid(s)

    print(s)

    ### case 1 & 2
    x = re.search("[Cc]ase.+linked to.+[cC]ase.+", s)
    if x:
        t = re.search("year-old", s)
        print("111111")


def process_file(filename):
    f = open(filename, "r")
    for line in f:
        if "linked to" in line:
            analyze_line(line)

process_file(sys.argv[1])