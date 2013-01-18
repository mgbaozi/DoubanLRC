#!/usr/bin/python
#coding: utf-8
from pymongo import MongoClient
class Singleton(type):
	_instances = {}
	def __call__(cls,*args,**kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)
		return cls._instances[cls]

class DbWork(object):
	__metaclass__ = Singleton
	def __init__(self):
		host = '127.0.0.1'
		try:
			client = MongoClient(host)
			db = client.douban_lrc
			self.posts = db.lrc
		except:
			self.posts = None
	
	def push(self,data):
		if not self.posts:
			return
		song = self.posts.find({'sid':data['sid']})
		if not song.count():
			self.posts.insert(data)
			return
		if not song[0]['lyric']:
			self.posts.update({'sid':data['sid']},data)
	
	def pull(self,sid):
		if not self.posts:
			return None
		return self.posts.find_one({'sid':sid})

