# coding: utf-8

from flask import (
    Flask, 
    request, 
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
import argparse
from flask_cors import CORS


import os
import datetime as dt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite'
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)


# ----------------------- data ------------------------

with open('data/image_list.txt') as f:
    image_list = [line.strip() for line in f]


class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(2048), unique=True)
    content = db.Column(db.String(1024))
    datetime = db.Column(db.Integer)
    is_marked = db.Column(db.Boolean)


# ------------------------ helper functions ------------------------

def makeUrl(ipAddress, port, staticFolder, filename):
    port = int(port)
    if port == 80:
        if staticFolder == '.':
            return "http://{}/{}".format(ipAddress, filename)
        else:
            return "http://{}/{}/{}".format(ipAddress, staticFolder, filename)
    else:
        if staticFolder == '.':
            return "http://{}:{}/{}".format(ipAddress, port, filename)
        else:
            return "http://{}:{}/{}/{}".format(ipAddress, port, staticFolder, filename)
        

def initDatabase(ipAddress, port, staticFolder):
    db.create_all()
    with open('./data/image_list.txt') as f:
        urls = [line.strip() for line in f]
    for idx, url in enumerate(urls):
        marker = Marker(id=idx, image_url=url, content=None, datetime=None, is_marked=False)
        db.session.add(marker)
    db.session.commit()


# -------------------------- route ----------------------------

@app.route('/captcha', methods=['GET'])
def get_next_image():
    markers = Marker.query.all()
    unmarked_markers = list(filter(lambda r: not r.is_marked, markers))
    if len(unmarked_markers) != 0:
        min_unmarked = min(unmarked_markers, key=lambda r: r.id)
        print('minId: ', min_unmarked.id)
        return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': {
                'imageUrl': image_list[min_unmarked.id],
                'imageId': min_unmarked.id
            }
        })
    else:
        return jsonify({
            'code': -1,
            'msg': 'no more Images',
            'data': ""
        })


@app.route('/mark', methods=['POST'])
def mark():
    try:
        data = request.get_json()
        marker = Marker.query.filter_by(id=data['imageId']).first()
        print(marker.id)
        marker.content = data['markValue']
        marker.datetime = int(dt.datetime.now().timestamp())
        marker.is_marked = True
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            'code': -1,
            'msg': 'internal error'
        })
    return jsonify({
            'code': 0,
            'msg': 'ok'
        })


@app.route('/init', methods=['GET'])
def init():
    markers = Marker.query.all()
    marked_markers = list(filter(lambda r: r.is_marked, markers))
    if len(marked_markers) != 0:
        max_id_marker = max(marked_markers, key=lambda r: r.id)
        return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': {
                'lastId': max_id_marker.id + 1,
                'totalImages': len(markers)
            }
        })
    else: 
        return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': {
                'lastId': 0,
                'totalImages': len(markers)
            }
        })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str)
    args = parser.parse_args()
    
    if args.mode == 'db':
        initDatabase('106.14.126.240', 80, '.')

    elif args.mode == 'app':
        app.run(host='0.0.0.0', port=1260, debug=True)
