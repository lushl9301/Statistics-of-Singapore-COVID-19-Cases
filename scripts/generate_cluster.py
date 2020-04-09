import sys
from common import *
import os
import csv

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
    if name.count(" ") > 4:
        s = name.split(" ")[0:5]
        name = " ".join(s)
    name2abv[name] = row[0]
    abv2name[row[0]] = row[1]


def process_file(filename):
    """

    :param f:
    :return:
    """
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

    # case 2: total of XXX confirmed cases^[\d+] now
    for line in processed_lines:
        m = re.search('(_.+?_)', line)
        if not m:
            continue
        abv = m.group(1)
        m = re.search("total of .+ cases\^", line)
        if not m:
            continue
        m = re.search("\^(\[\d+\])", line)
        ref = m.group(1)
        for t in processed_lines[::-1]:
            if ref in t:
                t = t[len(ref) + 1:]
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


files = os.listdir("raw_news")
files.sort()
for filename in files:
    print(filename)
    s = process_file(filename)
# s = process_file("2020-03-28.txt")
for item in cluster.items():
    print(abv2name[item[0]] + ",", sorted(item[1]))