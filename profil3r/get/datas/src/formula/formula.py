#!/usr/bin/python3
import sys
import os
from itertools import chain, combinations
from classes.core import Core
from classes.core.colors import Colors
from multiprocessing import Process

SETUP = './formula/setup.json'

def run(fullname):
    fullname = fullname.lower()
    fullname = fullname.split(" ")
    print("Input:", fullname)
    profil3r = Core(SETUP, fullname).run()
