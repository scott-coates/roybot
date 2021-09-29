from re import search
import praw
import config
import time
import redis
import csv
import urllib.request
import random

def bot_login():
	print("Logging in...")
	
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "The RoyBot Reddit Commenter v1.0")

	print("Logged in!")

	return r

def run_bot(r, conn, subreddit_to_search, search_str, replies):
	print("Searching last 1,000 comments")

	formatted_search_str = search_str.lower()
	
	for comment in r.subreddit(subreddit_to_search).comments(limit=1000):
		formatted_body_str = comment.body.lower()

		if formatted_search_str in formatted_body_str and not is_commented_replied_to(conn, comment.id) and comment.author != r.user.me():
			print(f"String with \"{formatted_search_str}\" found in comment {comment.permalink}.")
			
			comment_reply = get_comment_reply(replies)
			comment.reply(comment_reply)
			
			print("Replied to comment " + comment.permalink)

			record_commented_replied_to(conn, comment.id)

			# with open ("comments_replied_to.txt", "a") as f:
			# 	f.write(comment.id + "\n")

	print("Search Completed.")

	# print(comments_replied_to)

	print("Sleeping for 10 seconds...")
	#Sleep for 10 seconds...		
	time.sleep(10)


def is_commented_replied_to(conn, comment_id):
	ret_val = conn.sismember('comment_replies', comment_id)

	return ret_val

def record_commented_replied_to(conn, comment_id):
	ret_val = conn.sadd('comment_replies', comment_id)

	return ret_val

def get_comment_reply(replies):
	random_choice = random.choice(replies)[0]

	footers = [
		"I am a bot! Mention my name `RoyBot` whenever you need non-biased, third party arbitration to weigh in.",
		"I'm RoyBot! Mention my name `RoyBot` whenever you want a quote from the show. Now fuck off.",
		"This is RoyBot! Mention my name `RoyBot` whenever you attempt a hostile takeover.",
		"Hello! I am RoyBot! Mention my name `RoyBot` whenever you are the kin of neglectful billionaires and need a hug.",
	]

	# markdown - small font size
	footer = "^" + random.choice(footers).replace(' ', ' ^')

	ret_val = f"{random_choice}\n\n{footer}"

	return ret_val

def get_connection():
	r = redis.from_url(config.redis_url)

	return r

def get_replies():
	# get csv in py3 https://stackoverflow.com/questions/16283799/how-to-read-a-csv-file-from-a-url-with-python/62614979#62614979
	url = config.spreadsheet_url
	response = urllib.request.urlopen(url)
	lines = [l.decode('utf-8') for l in response.readlines()]
	cr = csv.reader(lines)

	# skip first line as header
	next(cr)
	ret_val = list(cr)

	return ret_val

# def get_saved_comments():
# 	if not os.path.isfile("comments_replied_to.txt"):
# 		comments_replied_to = []
# 	else:
# 		with open("comments_replied_to.txt", "r") as f:
# 			comments_replied_to = f.read()
# 			comments_replied_to = comments_replied_to.split("\n")
# 			comments_replied_to = filter(None, comments_replied_to)

# 	return comments_replied_to

conn = get_connection()
r = bot_login()
subreddit_to_search = config.subreddit
search_str = config.search_term
replies = get_replies()
#comments_replied_to = get_saved_comments()
# print(comments_replied_to)

while True:
	# run_bot(r, comments_replied_to)
	run_bot(r, conn, subreddit_to_search, search_str, replies)

