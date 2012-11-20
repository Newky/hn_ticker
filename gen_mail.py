#!/usr/bin/python2.6
from __future__ import with_statement

import datetime
import json
import os
import time

from optparse import OptionParser

HN_JSON_PATH = '/home/rdelaney/hn_json/'


def calculate_from_timestamp(timedelta):
	time_since = datetime.timedelta(timedelta)
	now = datetime.datetime.now()
	since_date = now - time_since
	return int(time.mktime(since_date.timetuple()))
	

def grab_file_names(from_timestamp):
	filenames = os.listdir(HN_JSON_PATH)
	timestamps = []
	for filename in filenames:
		if "_hn.json" in filename:
			timestamp = filename.replace('_hn.json', '')
			if from_timestamp <= int(timestamp):
				timestamps.append(timestamp)
	return timestamps

def get_links(fname):
	filename = '%s_hn.json' % fname
	filename = os.path.join(HN_JSON_PATH, filename)
	with open(filename, "rb") as inputfilename:
		content = inputfilename.read()
		if len(content) > 0:
			json_content = json.loads(inputfilename.read())
		return json_content


def print_link(link):
	print link["title"].encode('utf-8')
	print link["url"].encode('utf-8')
	print "http://news.ycombinator.com/item?id=%s" % (
		link["id"].encode('utf-8'))
	print link['score']
	print "-" * 200


def remove_duplicates(sorted_list, key='url'):
	exists = {}
	for link in sorted_list:
		if link == {}:
			continue
		url = link['url']
		if url in exists:
			if exists[url]["score"] < link['score']:
				exists[url]["score"] = link['score']
		else:
			exists[url] = link

	return exists.values()


def remove_after_time(entries, from_time):
	return [ entry for entry in entries
		if entry["unix_time"] < from_time]

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option('--days', dest='days',
		default=1, help='Number of days to be included in digest')
	(options, args) = parser.parse_args()
	timedelta = int(options.days) # days
	from_time = calculate_from_timestamp(timedelta)
	filenames = grab_file_names(from_time)
	links = []
	for filename in filenames:
		links += get_links(filename)
	links = remove_duplicates(links)
	links = remove_after_time(links, from_time)
	printed_links = sorted(links, key=lambda k: k['score'],
		reverse=True)
	printed_links = printed_links[:10]
	for link in printed_links:
		print_link(link)

