# coding: utf-8

from flask import (
    Flask, 
    request, 
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
import argparse
from flask_cors import CORS


import time
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
    is_marked = db.Column(db.Integer)


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


def clearSuspended():
    suspended_markers = Marker.query.filter(Marker.is_marked == 1).order_by(Marker.id, Marker.id.desc()).all()
    for suspended_marker in suspended_markers:
        now = dt.datetime.now().timestamp()
        if now - int(suspended_marker.datetime) > 60 * 60:
            suspended_marker.is_marked = 0
    db.session.commit()

# -------------------------- route ----------------------------

@app.route('/captcha', methods=['GET'])
def get_next_image():
    clearSuspended()
    marker = Marker.query.filter(Marker.is_marked == 0).order_by(Marker.id, Marker.id.desc()).limit(1).all()[0]
    if marker:
        marker.is_marked = 1
        marker.datetime = int(dt.datetime.now().timestamp())
        db.session.commit()
        return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': {
                'imageUrl': image_list[marker.id],
                'imageId': marker.id
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
        marker.is_marked = 2
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
    clearSuspended()
    marker = Marker.query.filter(Marker.is_marked == 0).order_by(Marker.id, Marker.id.desc()).limit(1).all()[0]
    markers = Marker.query.all()
    if marker:
        return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': {
                'lastId': marker.id,
                'totalImages':len(markers)
            }
        })
    else:

        return jsonify({
            'code': -1,
            'msg': 'no more Images',
            'data': {
                'lastId': 0,
                'totalImages': len(markers)
            }
        })


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--mode', type=str)
    # args = parser.parse_args()
    #
    # if args.mode == 'db':
    #     initDatabase('106.14.126.240', 80, '.')
    #
    # elif args.mode == 'app':
    app.run(host='0.0.0.0', port=1260)
