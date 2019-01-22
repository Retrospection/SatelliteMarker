# coding: utf-8
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


import sqlite3
import pathlib

conn = sqlite3.connect('/Users/retros/db.sqlite')
results = conn.execute("SELECT image_url, content FROM marker WHERE content <> '00000' AND content <> '' ")
with open('label.txt', 'w') as f:
    for result in results:
        if len(result[1]) == 5:
            f.write("{} {}\n".format(pathlib.Path(result[0]).name, result[1]))