import urllib
import urllib2

url = "https://api.groupme.com/v3/bots/post"
params = urllib.urlencode({
	"bot_id": "58ae5dfd7dfe0acde6da2340f2",
	"text": "Test"
})
reponse = urllib2.urlopen(url, params).read()