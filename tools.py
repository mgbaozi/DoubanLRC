#!/usr/bin/python
#coding: utf-8
import os
import random
class randbkg(object):
	#select a backgrount randomly from img/bg
	bglist = os.listdir('./static/img/bg')
	len =len(bglist)
	@classmethod
	def get(cls):
		return cls.bglist[int(random.random()*cls.len)]

from dbwork import DbWork
from searchlrc import *
import json

class GetLRC(object):
	"""get song_name and artist from request.form
	 delete chars like '(' to get result from internet
	 successfully,and then push the message of music 
	 which client request to DB"""
	@classmethod
	def getlrc(cls,form):
		sid = form.get('id')
		res = DbWork().pull(sid)
		if res:
			if res['lyric']:
				return json.dumps({'lyric':res['lyric'],'song_url':''})
		song_name = form.get('song_name')
		artist = form.get('artist')

		#delete string after special chars
		if '(' in song_name:
			song_name = song_name[:song_name.index('(')]
		if u'（' in song_name:
			song_name = song_name[:song_name.index(u'（')]
		if '-' in song_name:
			song_name = song_name[:song_name.index('-')]
		if '/' in artist:
			artist = artist[:artist.index('/')]
		song_name = song_name.strip()
		artist = artist.strip()
		try:
			res,song_url = FromBaidu.getlrc(song_name,artist)
		except:
			try:
				res,song_url = FromBaiduBackUp.getlrc(song_name,artist)
			except:
				try:
					res,song_url = FromFile.getlrc(song_name,artist)
				except:
					res = None
					song_url = None
		lrc = res if res else []
		song_url = song_url if song_url else ''
		#make sure lrc is lyric or empty list
		song_data = {'sid': form.get('id'),
					'title': song_name,
					'album': '',
					'artist': artist,
					'cover': form.get('cover'),
					'channel': form.get('channel'),
					'lyric': lrc}
		DbWork().push(song_data)	
		return json.dumps({'lyric':lrc,'song_url':song_url})
