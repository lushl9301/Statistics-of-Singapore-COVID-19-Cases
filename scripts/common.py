import re

def remove_age(s):
    return re.sub("\d+ year-old", "", s)


def remove_date(s):
    mth = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for m in mth:
        element = "\d+ to \d+ " + m + " 2020"
        t = re.sub(element, "", s)
        if t:
            s = t
        element = "\d+ to \d+ " + m + " 2019"
        t = re.sub(element, "", s)
        if t:
            s = t
        element = "\d+ to \d+ " + m
        t = re.sub(element, "", s)
        if t:
            s = t
        element = "\d+ to \d+ " + m
        t = re.sub(element, "", s)
        if t:
            s = t

    for m in mth:
        element = "\d+ " + m + " 2020"
        t = re.sub(element, "", s)
        if t:
            s = t
        element = "\d+ " + m + " 2019"
        t = re.sub(element, "", s)
        if t:
            s = t

    mth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m in mth:
        element = "\d+ " + m
        t = re.sub(element, "", s)
        if t:
            s = t
    return s

def remove_time(s):
    mth = ["pm", "am"]
    for m in mth:
        element = "\d+" + m
        t = re.sub(element, "", s, flags=re.I)
        if t:
            s = t
        element = "\d+" + m
        t = re.sub(element, "", s, flags=re.I)
        if t:
            s = t
    return s

def remove_covid(s):
    t = re.sub("2019-nCov", "", s, flags=re.I)
    if t:
        s = t
    t = re.sub("2019 novel", "", s, flags=re.I)
    if t:
        s = t
    t = re.sub("COVID-19", "", s, flags=re.I)
    if t:
        s = t
    t = re.sub("COVID 19", "", s, flags=re.I)
    if t:
        s = t
    return s

def replace_name(s, abv_dict):
    for item in abv_dict.items():
        s = s.replace(item[0], item[1])
    return s

def clean_line(s):
    s = s.strip()
    s = remove_age(s)
    s = remove_date(s)
    s = remove_time(s)
    s = remove_covid(s)
    return s
