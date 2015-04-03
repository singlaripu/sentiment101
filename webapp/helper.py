from info import classify2
from math import e
from datetime import datetime, timedelta
from email.utils import parsedate_tz
import time
from operator import itemgetter


def percentage_confidence(conf):
	return 100.0 * e ** conf / (1 + e**conf)


def get_sentiment_info(text):
	flag, confidence = classify2(text)
	if confidence > 0.5:
		sentiment = "Positive" if flag else "Negative"
	else:
		sentiment = "Neutral"
	conf = "%.0f" % percentage_confidence(confidence)
	return (sentiment, conf)

def get_time_difference(datestring):
	time_tuple = parsedate_tz(datestring.strip())
	delta = datetime.utcnow() - datetime(*time_tuple[:6])
	epoch = time.mktime(time.strptime(datestring,"%a %b %d %H:%M:%S +0000 %Y"))
	
	if delta.days // 365:
		return str(delta.days // 365) + " years ago", epoch

	if delta.days:
		return str(delta.days) + " days ago", epoch

	if delta.seconds // 3600:
		return str(delta.seconds // 3600) + " hours ago", epoch

	if delta.seconds // 60:
		return str(delta.seconds // 60) + " minutes ago", epoch

	if delta.seconds:
		return str(delta.seconds) + " seconds ago", epoch


def score(tweets):
	positive = negative = neutral = 0
	for tweet in tweets:
		tweet['sentiment'], tweet['confidence'] = get_sentiment_info(tweet['text'])
		tweet['created_at'], tweet['epoch'] = get_time_difference(tweet['created_at'])
		tweet['confidence'] += '%'

		if tweet['sentiment'] == 'Positive':
			positive += 1
		elif tweet['sentiment'] == 'Negative':
			negative += 1
		else:
			neutral += 1

	tweets = sorted(tweets, key=itemgetter('epoch'), reverse=True)
	return tweets, [positive, negative, neutral]
