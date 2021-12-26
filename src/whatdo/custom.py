#!/usr/bin/env python3

from dataclasses import dataclass

from whatdo.utils import load_games

cache = None
file = "custom.json"

def games() -> dict:
    global cache
    if cache is not None:
        return cache
    try:
        cache = load_games(file)
    except FileNotFoundError:
        print("No custom games exist yet, start by adding some")
        cache = {}
    return cache

@dataclass
class custom_entry:
    appid: int
    name: str
    
