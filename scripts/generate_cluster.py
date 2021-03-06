from common import *
import os
import csv
import networkx as nx
import matplotlib.pyplot as plt

from random import seed
from random import randint
import math
# seed random number generator
seed(0)


name2abv = {}
abv2name = {}
cluster = {}
## hard code
cluster['_lfc_'] = {8, 9}
## hard code
try:
    f = open('../data/cluster_label.csv', newline='')
except:
    f = open('data/cluster_label.csv', newline='')
reader = csv.reader(f)
next(reader, None)
for row in reader:
    name = row[1]
    if name.count(" ") >= 4:
        s = name.split(" ")[0:4]
        name = " ".join(s)
    name2abv[name] = row[0]
    abv2name[row[0]] = row[1]


def process_file(filename):
    """

    :param f:
    :return:
    """
    try:
        filename = "../raw_news/" + filename
        f = open(filename, "r")
    except:
        filename = "raw_news/" + filename
        f = open(filename, "r")
    lines = f.readlines()
    processed_lines = []
    for line in lines:
        line = clean_line(line)
        line = replace_name(line, name2abv)
        processed_lines.append(line)

    # case 1: total of XXX confirmed cases now (Case [\d+,,]+)
    for line in processed_lines:
        m = re.search('(_.+?_)', line)
        if not m:
            continue
        abv = m.group(1)
        m = re.search("total of .+ cases now", line)
        if not m:
            continue
        m = re.search('(\(Case.+?\))', line)
        if not m:
            print(line)
        s = m.group(1)
        case_l = [int(x) for x in re.findall(r"\d+", s)]
        try:
            cluster[abv].update(case_l)
        except:
            cluster[abv] = set(case_l)
    try:
        print(">>>>> ", cluster["_snk_"])
    except:
        pass
    # case 2: total of XXX confirmed cases^[\d+] now
    for line in processed_lines:
        m = re.search('(_.+?_)', line)
        if not m:
            print(line)
            continue
        abv = m.group(1)
        m = re.search("total of .+ cases\^", line)
        n = re.search(" previous cases\^", line)
        l = re.search(" confirmed cases\^", line)
        if (not m) and (not n) and (not l):
            continue
        m = re.search("\^(\[\d+\])", line)
        try:
            ref = m.group(1)
        except:
            m = re.search("(\^\d+)", line)
            ref = m.group(1)
        for t in processed_lines[::-1]:
            if ref in t:
                t = t[len(ref) + 1:]
                t = t[t.find(":") + 1 :]
                case_l = [int(x) for x in re.findall(r"\d+", t)]
                try:
                    cluster[abv].update(case_l)
                except:
                    cluster[abv] = set(case_l)
                break

    # case 3: .+ (Case[s] [\d+,,]+) is / are linked to xxx
    for line in processed_lines:
        sentence = re.findall('\(Case.+? linked to .+?\.+?', line)
        for s in sentence:
            m = re.search('(_.+?_)', s)
            if not m:
                continue
            abv = m.group(1)
            m = re.search('(\(Case.+?\))', s)
            cases = m.group(1)
            case_l = [int(x) for x in re.findall(r"\d+", cases)]
            try:
                cluster[abv].update(case_l)
            except:
                cluster[abv] = set(case_l)

    # case 4: (Case[s] [\d+,,]+) is / are linked to .+ previous case[s] (Case[s] [\d+,,]+), forming a new cluster at xxxx
    for line in processed_lines:
        sentence = re.findall('(\(Case.+?\).+?linked to.+?previous.+?\(Case.+?\).+?)(_.+?_)', line)
        if not sentence:
            continue
        if len(sentence) > 1:
            print("===== XXX more than 1 matching")
        s = sentence[0][0]
        abv = sentence[0][1]
        s = re.findall('(\(Case.+?\))', s)
        case_l = []
        for cases in s:
            case_l += [int(x) for x in re.findall(r"\d+", cases)]
        try:
            cluster[abv].update(case_l)
        except:
            cluster[abv] = set(case_l)

try:
    files = os.listdir("../raw_news")
except:
    files = os.listdir("raw_news")
files.sort()
for filename in files:
    print(filename)
    s = process_file(filename)
# s = process_file("2020-04-14.txt")
cluster_md = open("existing_clusters_list.md", "w")
for item in cluster.items():
    cluster_md.write("### " + abv2name[item[0]] + "\n\n")
    cluster_md.write("Cases " + ", ".join([str(x) for x in sorted(item[1])]) + "\n\n")

## draw clustering
G = nx.Graph()
for item in cluster.items():
    G.add_node(abv2name[item[0]])
    for i in item[1]:
        G.add_node(i)
        G.add_edge(abv2name[item[0]], i)#, weight=randint(1, 10) * 300)

graph_pos = nx.spring_layout(G, scale=50, k=1.5/math.sqrt(G.order()))

cl = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
c = 0
for item in cluster.items():
    nx.draw_networkx_nodes(G,graph_pos,
                       nodelist=[abv2name[item[0]]],
                       node_color='grey',
                       # node_size=1000,
                   alpha=0.2)
    nx.draw_networkx_labels(G, graph_pos, labels={abv2name[item[0]] : abv2name[item[0]]}, font_size=5, font_family='sans-serif')

    nx.draw_networkx_nodes(G,graph_pos,
                       nodelist=sorted(item[1]),
                       node_color=cl[c],
                       node_size=15,
                   alpha=0.6)
    nx.draw_networkx_labels(G, graph_pos, labels=dict(zip(sorted(item[1]), sorted(item[1]))), font_size=1, font_family='sans-serif')
    c = (c + 1) % 10
options = {
    'node_color': 'black',
    'node_size': 5,
    'line_color': 'grey',
    'linewidths': 0,
    'width': 0.1,
}

# nx.draw_networkx_nodes(G, graph_pos, node_size=1, node_color='blue', alpha=0.3)
nx.draw_networkx_edges(G, graph_pos, width=0.5, alpha=0.7)

plt.savefig('cluster_visualization.png', dpi=1000)
plt.savefig('cluster_visualization.pdf')
