import kdapi
import praw

score = 0
url = None
itemList =  kdapi.check("http://i.imgur.com/nn5UneG.gif")
print len(itemList)
for item in itemList:
    print item.title
    if score < item.score:
        print item.score
        score = item.score
        url = item.link
    if item.similarity > 98:
        print "yes"
print url
FirstSplitUrl = url.split("/comments/")
SecondSplitUrl = FirstSplitUrl[1].split("/")
SubmissionID = SecondSplitUrl[0]
print SubmissionID
r = praw.Reddit('Comment Scraper 1.0 by u/_Daimon_ see '
                'https://praw.readthedocs.org/en/latest/'
                'pages/comment_parsing.html')
submission = r.get_submission(submission_id=SubmissionID)
CommentList = submission.comments
TopComment = CommentList[0].body
print TopComment


