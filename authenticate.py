import praw
import OAuth2Util


user_agent = 'Post Smart Comments see https://github.com/nikhil for the source'
r = praw.Reddit(user_agent)
o = OAuth2Util.OAuth2Util(r)

