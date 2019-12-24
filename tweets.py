# tweets.py: Twitter crawler 

import tweepy
import json
# to disable pip warning message
import requests.packages.urllib3
import sys
import time
import os
import logging
import threading

exitFlag = 0

#get command line arguements
if len(sys.argv) < 4:
	print 'Missing either [seed Twitter name] [per user tweet count] [output directory path] on the command line.'
	sys.exit(1)

seed = sys.argv[1]#seed user name
tweet_count = sys.argv[2] #per user
output_dir = sys.argv[3] #output directory
	

#creating new class
#class twitterThread (threading.Thread):
#	def __init__(self, label, filename):
#		threading.Thread.__init__(self)
#		self.label = label
#		self.filename = filename
#	def run(self):
#		try:
#			time.sleep(2)
#			print 'Starting thread ' + str(self.label + 1)
#			collect(self.label, self.filename)
#			print 'Exiting thread ' + str(self.label + 1)
#		except Exception:
#			print sys.exc_info()
#			raise

# addressing tweepy.logger issues
logging.basicConfig()

# to disable pip warning message
requests.packages.urllib3.disable_warnings()

consumer_key = 'JSNXqpcRBmME2SVODoDABy3pW'
consumer_secret = 'iHaos7bkFq4DOUBx15rFUJ6T5U3k9owGwMKuZGf6KdGpLQOkGU'
access_token = '1089890772151820288-6fKqE7VKbbloc9xQLkGTHkNl9r5cyy'
access_token_secret = 'LLjwWh61fBZlijwNoAtWu13BuuiFYFmzfsgwCr8nICGbM'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

try:
	redirect_url = auth.get_authorization_url()
except:
	print ('Error! Failed to get request token')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

username = seed
try:
	user = api.get_user(username)
except tweepy.TweepError:
	print "Error: couldn't get user"
	exit(1)

#print "user: ", user.screen_name
#print "follower count: ", user.followers_count
			
#def collect(label, outfile):
i = 0
tweet_count = 0
seen_followers = []
twts = []
jfile = output_dir + '/tweets.json'
with open(jfile, 'w') as f:
	try:
		try:
			for follower in tweepy.Cursor(api.followers, screen_name=user.screen_name).items():
			#tweepy.Cursor(api.followers, screen_name=user.screen_name).items():
				try:
					if i % 1000 == 0:
						print 'Size of ' + jfile + ': ' + str(os.stat(jfile).st_size / float(1000000)) + ' MB'

					i = i + 1
					user_location = ""

					#if follower.location != "":
						#continue
					#else:
						#user_location = (follower.location).encode('utf-8')
						#print "follower location: ", follower.location

					if seen_followers.count(follower) > 0:
						continue
					
					#if i % 5 == label:
					try:
						seen_followers.append(follower)
						for tweet in api.user_timeline(follower.screen_name, count=tweet_count):
				
							try:

								#only grab tweets when place is not None
								#if tweet.place != None:
										
								tweet_count = tweet_count + 1
								twt = json.dumps(tweet._json)
								#print "Tweet location: ", tweet.place
								twts.append(twt)

								if len(twts) > 1000:
									for te in twts:
										f.write(te+'\n')

									twts = []
									

								f.flush() # to ensure everything written to disk

							except tweepy.RateLimitError:
								f.flush()
								print 'Rate limit reached. Sleeping 15 minutes...'
								time.sleep(15*60)
					except tweepy.RateLimitError:
						f.flush()
						print 'Rate limit reached. Sleeping 15 minutes...'
						time.sleep(15*60)
					except tweepy.TweepError:
						print '\t' + follower.screen_name + ' has protected tweets[. Skipping...'

				except tweepy.RateLimitError:
					f.flush()
					print 'Rate limit reached. Sleeping 15 minutes...'
					time.sleep(15*60)
		except tweepy.RateLimitError:
			f.flush()
			print 'Rate limit reached. Sleeping 15 minutes...'
			time.sleep(15*60)
		except tweepy.TweepError:
			print follower.screen_name + ' has a private account. Skipping...(sleeping)'
	except KeyboardInterrupt:
		print '\nKeyboard Interrupt: Everything should be written to file'
		f.flush()

print 'Size of ' + jfile + ': ' + str(os.stat(jfile).st_size / float(1000000)) + ' MB'
print seed + '\'s followers list exhausted. Done.'
