import urllib
import json
import re

response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft&rpp=10&page=6")
tweetDict = json.load(response)

reg = re.compile('Bing')

for t in tweetDict['results']:
    print "user: %s\n%s\n" % (t['from_user'], t['text'])
