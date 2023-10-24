import os
import sys
import random

'''GLOBALS'''
usedSeed: list
inPath: str
outPath: str


def set_in_path(path: str):
    inPath = path


def set_out_path(path: str):
    outPath = path


# Get SD model path via env.vars
def get_model(model: str):
    return os.getenv(model)


# Increasing linearly
def generate_seed():
    seed = random.randint(0, sys.maxsize)
    while seed in usedSeed:
        seed = random.randint(0, sys.maxsize)
    usedSeed.append(seed)
    return seed
