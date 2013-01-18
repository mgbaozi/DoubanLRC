#!/usr/bin/python
#coding: utf-8
import urllib2
import cookielib
import json
from xml.dom import minidom
from formatlrc import FormatLRC

class FromBaidu(object):
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	@classmethod
	def getlrc(cls,song_name,artist):
		url = 'http://sug.music.baidu.com/info/suggestion?format=json&word=' +\
			  urllib2.quote(song_name.encode('utf-8')) + '-' + \
			  urllib2.quote(artist.encode('utf-8'))
		req = cls.opener.open(url)
		content = json.loads(req.read())
		songid = content[u'song'][0][u'songid']
		url = 'http://play.baidu.com/data/music/songlink?songIds=' + \
			  urllib2.quote(songid) + '&type=mp3'
		req = cls.opener.open(url)
		content = json.loads(req.read())
		lrc_url = content[u'data'][u'songList'][0][u'lrcLink']
		mp3_url = content[u'data'][u'songList'][0][u'showLink']
		lrc_url = 'http://music.baidu.com' + lrc_url
		req = cls.opener.open(lrc_url)
		lrc = req.read()
		return FormatLRC(lrc),mp3_url


class FromBaiduBackUp(object):
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	@staticmethod
	def getmp3url(doc):
		part1 = doc.getElementsByTagName('encode')[0].firstChild.nodeValue
		part2 = doc.getElementsByTagName('decode')[0].firstChild.nodeValue
		part1 = part1[9:-3]
		part2 = part2[9:-3]
		return part1 + part2
	@classmethod
	def getlrc(cls,song_name,artist):
		url = 'http://box.zhangmen.baidu.com/x?op=12&count=1&title=' + \
			  iurllib2.quote(song_name.encode('utf-8')) + '$$' + \
			  urllib2.quote(artist.encode('utf-8')) + '$$$$'
		req = cls.opener.open(url)
		content = req.read().decode('gb2312')
		content = content.replace(u'gb2312',u'utf-8')
		doc = minidom.parseString(content)
		lrc_id = int(doc.getElementsByTagName("lrcid")[0].firstChild.nodeValue)
		try:
			mp3_url = getmp3url(doc)
		except:
			mp3_url = None
		lrc_url = 'http://box.zhangmen.baidu.com/bdlrc/' + str(lrc_id/100) \
				  + '/' + str(lrc_id) + '.lrc'
		req_lrc = cls.opener.open(lrc_url)
		lrc = req_lrc.read().decode('gb2312').encode('utf-8')
		return FormatLRC(lrc), mp3_url

