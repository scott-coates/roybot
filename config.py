import os

try:
    # https://github.com/theskumar/python-dotenv
    # todo make multi env https://stackoverflow.com/questions/17803829/how-to-customize-a-requirements-txt-for-multiple-environments
    from dotenv import load_dotenv
    load_dotenv()  # take environment variables from .env.
    # Code of your application, which uses environment variables (e.g. from `os.environ` or
    # `os.getenv`) as if they came from the actual environment.
except:
    pass

subreddit = os.environ['SUBREDDIT']
search_term = os.environ['SEARCH_TERM']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
redis_url = os.environ['REDIS_URL']
