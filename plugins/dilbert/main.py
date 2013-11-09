def enabled():
	return True

def title():
	return "Dilbert"

def subtitle():
	return "View Dilbert's daily strip"

def run():
	import feedparser
	import os
	d = feedparser.parse('http://dilbert.com/fast')
	strip = [i[5:-1] for i in d['feed']['summary'].split() if i.find('str_strip') > 0][0]
	os.system('curl -s ' + strip + ' --O strip.png')
	os.system('qlmanage -p strip.png')
