import os

from flask import Flask, request, jsonify

from service import fill_comp_style as fcs
from service import fill_feat as ff
from service import map_tag as mt1
from service import map_xpath as mx1
from service import dd_to_tm

app = Flask(__name__)


@app.route('/dir-maker', methods=["POST"])
def dir_maker():
    try:
        if request.method == "POST":
            ls = request.json['folder_name']
            loc = request.json['loc']
            for x in ls:
                for item in ['xml', 'excel', 'word', 'pdf', 'res']:
                    os.makedirs(f'{loc}/{x}/{item}', exist_ok=True)
                os.makedirs(f'{loc}/{x}/xml/ox_{x}', exist_ok=True)
                os.makedirs(f'{loc}/{x}/xml/cx_{x}', exist_ok=True)
                os.makedirs(f'{loc}/{x}/xml/zx_{x}', exist_ok=True)
            return {'folder_name': ls, 'loc': loc, 'status': 'created'}
    except Exception as e:
        return jsonify({'status': str(e)})


@app.route("/map-xpath", methods=["POST"])
def map_xpath():
    try:
        if request.method == "POST":
            loc = request.json['loc']
            ct = request.json['ct']
            file_name = request.json['file_name']
            sn = request.json['sn']
            res = mx1.map_xpath_to_tag(loc, ct, file_name, sn)
            return {'status': res}
    except Exception as e:
        return jsonify({'status': str(e)})


@app.route("/fill-tm-by-dd", methods=["POST"])
def fill_tm_by_dd():
    try:
        if request.method == "POST":
            loc = request.json['loc']
            ct = request.json['ct']
            res = dd_to_tm.fill_tm_by_dd(loc, ct)
            return {'status': res}
    except Exception as e:
        return jsonify({'status': str(e)})


@app.route("/map-tag", methods=["POST"])
def map_tag():
    try:
        if request.method == "POST":
            loc = request.json['loc']
            ct = request.json['ct']
            res = mt1.map_tag(loc, ct)
            return {'status': res}
    except Exception as e:
        return jsonify({'status': str(e)})


@app.route("/fill-feat", methods=["POST"])
def fill_feat():
    try:
        if request.method == "POST":
            loc = request.json['loc']
            ct = request.json['ct']
            ls = ff.fill_feature(loc, ct)
            return {'xpath': ls}
    except Exception as e:
        return jsonify({'status': str(e)})


@app.route("/fill-comp-style", methods=["POST"])
def fill_comp_style():
    try:
        if request.method == "POST":
            loc = request.json['loc']
            ct = request.json['ct']
            ls, fc = fcs.fill_comp_style(loc, ct)
            return {'xpath_left': ls, 'false_count': fc}
    except Exception as e:
        return jsonify({'status': str(e)})


if __name__ == '__main__':
    app.run()
