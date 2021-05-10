import requests
from requests.exceptions import HTTPError

import csv
import os, sys
from PIL import Image
import glob
import json
from collections import OrderedDict
from pymongo import MongoClient
from os import path

import random
from pathlib import Path
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

path = Path(__file__).parent / "../../core/RM_Trivia.csv"
with path.open(encoding="utf8") as f:

    a = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

    random_trivia = random.randint(0,len(a)-1)
    while a[random_trivia]['Trivia']=='':
        random_trivia = random.randint(0,len(a)-1)

    print(uprint(a[random_trivia]['Trivia']))






