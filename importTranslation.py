#!/usr/bin/python3
__author__ = "dgideas@outlook.com"

import pymongo
import sys
import json

def main():
	filename = sys.argv[1]
	print("正在处理文件", filename)
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["taas"]
	coll = db["translate"]
	print("翻译数据库现有记录", coll.count(), "条")
	lineCnt = 0
	dumplicateCnt = 0
	insertionCnt = 0
	with open(filename, "r") as f:
		for line in f:
			line = line.replace("\n", "")
			if line != "":
				line = json.loads(line)
				lineCnt += 1
				if coll.count({"text": line["text"]}):
					dumplicateCnt += 1
				else:
					coll.insert_one(line)
					insertionCnt += 1
				print("\r" + str(lineCnt), end="")
	print("")
	print("共计", lineCnt, "行，其中重复项", dumplicateCnt, "行，新插入了", insertionCnt, "行;")
	print("\t目前共有记录", coll.count(), "条")

if __name__ == "__main__":
	main()
