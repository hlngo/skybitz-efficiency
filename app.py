#!flask/bin/python
# app.py is for the flask portion of the this efficiency app

from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


# Flask Run
@app.route('/', methods=['GET'])
def index():
    return 'nothing to see here'

@app.route('/effit', methods=['GET'])
def effit():
    with open('simpledata.json', 'r') as jfile:
        data = json.load(jfile)
    
    #return jsonify({'data': data})
    return jsonify(data)

if __name__ == '__main__':
    app.run()
