from flask import Flask, render_template, request, jsonify
import pickle
import random
import json
import urllib2
import fetch
app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/search')
def search():
	queryStr = request.args.get('query')

	results = fetch.fetch(queryStr)

	return render_template('results.html', queryStr=queryStr, results=results)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=13001)
