# coding: utf-8

from flask import (
    Flask, 
    request, 
    jsonify,
    send_file
)
from flask_sqlalchemy import SQLAlchemy
import argparse
from flask_cors import CORS


import os


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
    images = os.listdir('./images')
    urls = [makeUrl(ipAddress, port, staticFolder, image) for image in images]
    for idx, url in enumerate(urls):
        marker = Marker(id=idx, image_url=url, content=None, datetime=None, is_marked=False)
        db.session.add(marker)
    db.session.commit()


# -------------------------- route ----------------------------

@app.route('/captcha/<int:id>', methods=['GET'])
def get_next_image(id):
    print(id)
    if id >= len(image_list):
        return jsonify({
            'code': -1,
            'msg': 'image not found',
            'data': ''
        })
    return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': image_list[id]
        })

@app.route('/mark', methods=['POST'])
def mark():
    data = request.get_json()
    imageId = data['imageId']
    
    pass


@app.route('/init', methods=['GET'])
def init():
    markers = Marker.query.all()
    markedMarkers = filter(lambda r: r.is_marked, markers)
    if list(markedMarkers):
        maxIdMarker = max(markedMarkers, key=lambda r: r.id)
        return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': {
                'lastId': maxIdMarker.id + 1,
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
        initDatabase('127.0.0.1', 30901, '.')

    elif args.mode == 'app':
        app.run(host='0.0.0.0', port=1260)
