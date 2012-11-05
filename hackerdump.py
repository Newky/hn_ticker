#!/usr/bin/python2.6
import json

from pyhackerstories import _get_page, _extract_stories, hacker_url

def story_to_dict(story):
	elements = ['position', 'id', "title", "url", "user", "score",
		"human_time", "unix_time", "comments"]
	story_dict = dict([
		(element, getattr(story, element)) for element in elements])
	return story_dict


if __name__ == '__main__':
	content = _get_page(hacker_url)
	entries = _extract_stories(content)
	for pos, story in enumerate(entries):
		story.position = pos+1
	dict_entries = [
		story_to_dict(entry) for entry in entries]
	print json.dumps(dict_entries, indent=4)


