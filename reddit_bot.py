from re import search
import praw
import config
import time

def bot_login():
	print("Logging in...")
	
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "The RoyBot Reddit Commenter v1.0")

	print("Logged in!")

	return r

def run_bot(r, subreddit_to_search, search_str):
	print("Searching last 1,000 comments")

	formatted_search_str = search_str.lower()
	
	for comment in r.subreddit(subreddit_to_search).comments(limit=1000):
		formatted_body_str = comment.body.lower()

		if formatted_search_str in formatted_body_str and not is_commented_replied_to(comment.id) and comment.author != r.user.me():
			print(f"String with \"{formatted_search_str}\" found in comment {comment.permalink}.")
			
			comment_reply = get_comment_reply()
			comment.reply(comment_reply)
			
			print("Replied to comment " + comment.permalink)

			record_commented_replied_to(comment.id)

			# with open ("comments_replied_to.txt", "a") as f:
			# 	f.write(comment.id + "\n")

	print("Search Completed.")

	# print(comments_replied_to)

	print("Sleeping for 10 seconds...")
	#Sleep for 10 seconds...		
	time.sleep(10)


def is_commented_replied_to(comment_id):
	return False

def record_commented_replied_to(comment_id):
	return False


def get_comment_reply():
	return "hi"

# def get_saved_comments():
# 	if not os.path.isfile("comments_replied_to.txt"):
# 		comments_replied_to = []
# 	else:
# 		with open("comments_replied_to.txt", "r") as f:
# 			comments_replied_to = f.read()
# 			comments_replied_to = comments_replied_to.split("\n")
# 			comments_replied_to = filter(None, comments_replied_to)

# 	return comments_replied_to


r = bot_login()
subreddit_to_search = config.subreddit
search_str = config.search_term
#comments_replied_to = get_saved_comments()
# print(comments_replied_to)

while True:
	# run_bot(r, comments_replied_to)
	run_bot(r, subreddit_to_search, search_str)

