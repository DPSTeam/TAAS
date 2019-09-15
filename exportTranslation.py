#!/usr/bin/python3
__author__ = "dgideas@outlook.com"

import pymongo
import sys
import json

def main():
	jsonDumpFile = open("translate_dump.json", "w")
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["taas"]
	coll = db["translate"]
	a = input("共计搜索到" + str(coll.count()) + "条翻译，是否继续导出?(Ctrl+C Exit)")
	for item in coll.find():
		item.pop("_id")
		jsonDumpFile.write(json.dumps(item, ensure_ascii=False) + "\n")
	jsonDumpFile.close()

if __name__ == "__main__":
	main()
