#!/usr/bin/python3
__author__ = "dgideas@outlook.com"

import pika
import pymongo
import json
from lang import langList
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def homepage():
	usage = '<h1>Usage</h1><hr/><p>./translate?text=xxx&sl=zh-CN&tl=en</p><hr/><p><strong>Author</strong>:' + __author__ + "</p>"
	return usage

@app.route("/translate")
def taasTranslateAsync():
	text = request.args.get('text', None)
	sourceLanguage = request.args.get('sl', None)
	targetLanguage = request.args.get('tl', None)
	
	warningMsg = ""
	if text is None:
		warningMsg += "<p>Argument <strong>text</strong> can't be empty.</p>"
	if sourceLanguage is None:
		warningMsg += "<p>Argument <strong>sl</strong> can't be empty.</p>"
	if targetLanguage is None:
		warningMsg += "<p>Argument <strong>tl</strong> can't be empty.</p>"
	text = str(text)
	sourceLanguage = str(sourceLanguage)
	targetLanguage = str(targetLanguage)
	if sourceLanguage not in langList:
		warningMsg += "<p>" + sourceLanguage + " in <strong>sl</strong> is not an avalible language option.</p>"
	if targetLanguage not in langList:
		warningMsg += "<p>" + targetLanguage + " in <strong>tl</strong> is not an avalible language option.</p>"
	if len(warningMsg):
		return "<h1>Warning</h1><hr/>" + warningMsg
	
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["taas"]
	coll = db["translate"]
	result = coll.find_one({"text": text, "sl": sourceLanguage, "tl": targetLanguage}, {"res": 1})
	if result is not None:
		return json.dumps({"status": "ok", "res": result["res"]}, ensure_ascii=False)
	
	parameters = pika.ConnectionParameters()
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.queue_declare(queue="taas", durable=True, exclusive=False, auto_delete=False)
	channel.basic_publish(exchange='', routing_key='taas',
						body=json.dumps({"text": text, "sl": sourceLanguage, "tl": targetLanguage}, ensure_ascii=False))
	connection.close()
	return json.dumps({"status": "queued", "res": None}, ensure_ascii=False)

if __name__ == '__main__':
	app.run(host="0.0.0.0")