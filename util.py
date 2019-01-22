# coding: utf-8

import sqlite3
__SQL = """
    UPDATE marker SET id = {}, image_url = '{}', content = '{}', datetime = '{}', is_marked = {} where id={}
"""

if __name__ == '__main__':
    origin = sqlite3.connect('./data/_db.sqlite')
    now = sqlite3.connect('./data/db.sqlite')
    results = origin.execute('select * from marker')
    newResults = [(result[0], result[1], result[2] if result[2] else '', result[3] if result[3] else '', 2 if result[4] else 0) for result in results]
    for newResult in newResults:
        string = __SQL.format(newResult[0], newResult[1], newResult[2], newResult[3], newResult[4], newResult[0])
        print(string)
        now.execute(string)
    now.commit()