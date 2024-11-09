import requests
from bs4 import BeautifulSoup
import json
import pprint
from random import randrange
import time

def parse_json(url: str):
    r = requests.get(url)

    if r.ok == False:
        return (False, None)

    try:
        soup = BeautifulSoup(r.content, features="html.parser")
    except Exception as e:
        print(e)
        print(r.content)
        return (False, None)
    scripts = soup.select('script[type="application/ld+json"]')
    result = []

    for i in range(len(scripts)):
        script = scripts[i]
        try:
            result.append(json.loads(script.get_text()))
        except Exception as e:
            print(e)
            result.append(None)
    return (True, result)

def read_state():
    with open("data/parsing/state.json") as f:
        return json.load(f)

def write_file(path, data):
    with open(path, "w") as f:
        # f.write(pprint.pformat(data, compact=True).replace("'",'"'))
        json.dump(data, f)

def write_state(state):
    write_file("data/parsing/state.json", state)

def read_state_or_default():
    try:
        return read_state()
    except Exception as e:
        print(e)
        write_state({
            "queued": [],
            "finished": []
        })
        return read_state()

state = read_state_or_default()

def recursive_extract_string_values(value, result=[]):
    if isinstance(value, dict):
        for ivalue in value.values():
            recursive_extract_string_values(ivalue, result)
    elif isinstance(value, list):
        for ivalue in value:
            recursive_extract_string_values(ivalue, result)
    else:
        result.append(value)
    return result


def filter_out(state, data):
    values = map(lambda o: recursive_extract_string_values(o, []) if isinstance(o, dict) else None, data)
    values = filter(lambda s: s.startswith("https://www.epicurious.com/") if isinstance(s, str) else False, sum(values, []))
    values = filter(lambda s: s not in state["queued"] or s not in state["finished"], values)
    values = filter(lambda s: "search" not in s, values)
    values = filter(lambda s: not s.endswith(".png"), values)
    values = filter(lambda s: not s.endswith(".jpg"), values)
    return list(values)


def recursive_parse(start_url: str):
    state = read_state_or_default()
    (success, data) = parse_json(start_url)
    state["queued"] += filter_out(state, data)
    write_state(state)
    while len(state["queued"]) != 0:
        url = state["queued"][0]
        print("parsing", url)
        (success, data) = parse_json(url)
        if success:
            write_file("data/parsing/" + url.replace("/", "_") + ".json", data)
        state["queued"].remove(url)
        state["finished"].append(url)
        write_state(state)
        time.sleep(randrange(4))



# pprint.pp(recursive_parse("https://www.epicurious.com/"))

# print(parse_json('https://www.epicurious.com/recipes/food/views/no-bake-mangonada-bars'))