#!/usr/bin/env python3

import random
# some util function to assist me

def build_request(url: str, location: str, options: dict) -> str:
    req = url + location + "?"
    for key,value in options.items():
        req += key + "=" + value + "&"
    return req[0:-1]

def get_random(choices: list):
    while True:
        erg = random.choice(choices)
        if "exclude" not in erg or erg["exclude"] == False:
            return erg

def col(color: str) -> str: # wen ich fancy sein will can hier auf color support getestet werden
    return color
