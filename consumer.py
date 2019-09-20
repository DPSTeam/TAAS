#!/usr/bin/python3
__author__ = "dgideas@outlook.com"

import json
import pika
import sys
from googletrans import Translator
import time
import pymongo

translator = Translator(service_urls=['translate.google.com'])

def taas_translate_async(channel, method_frame, header_frame, body):
	msg = json.loads(body)
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["taas"]
	coll = db["translate"]
	result = coll.find_one({"text": msg["text"], "sl": msg["sl"], "tl": msg["tl"]}, {"res": 1})
	if result is not None:
		# Already translated
		channel.basic_ack(delivery_tag=method_frame.delivery_tag)
		return
	
	while True:
		try:
			time.sleep(10)
			res = translator.translate(msg["text"], src=msg["sl"], dest=msg["tl"]).text
			print("Translated", msg["text"], "from", msg["sl"], "to", msg["tl"])
			break
		except KeyboardInterrupt:
			print("KeyboardInterrupt")
			sys.exit()
		except:
			time.sleep(10)
			continue
	coll.insert_one({"text": msg["text"], "sl": msg["sl"], "tl": msg["tl"], "res": res})
	channel.basic_ack(delivery_tag=method_frame.delivery_tag)
	return

def main():
	parameters = pika.ConnectionParameters()
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.queue_declare(queue="taas", durable=True, exclusive=False, auto_delete=False)
	channel.basic_qos(prefetch_count = 100)
	channel.basic_consume('taas', taas_translate_async)
	try:
		channel.start_consuming()
	except KeyboardInterrupt:
		channel.stop_consuming()
	connection.close()

if __name__ == "__main__":
	main()
