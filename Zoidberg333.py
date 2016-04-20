import os
import praw
import requests
import OAuth2Util
from urlparse import urlparse
from pymongo import MongoClient
import datetime
import time
import sendgrid
import json
import sys
import kdapi
import traceback


def CallKdapi(SearchUrl):
    itemDict =  kdapi.check(SearchUrl)
    itemList = itemDict['output']
    itemTime = itemDict['time']
    length = len(itemList)
    print "finished"
    if length == 0:
        return {'ID':'Empty'}
    if length == 1:
        if itemList[0].similarity == None:
            return {'ID':'Empty'}
    score = 0
    url = None
    for item in itemList:
        if item.similarity != None:
            #print item.title
            if item.similarity > 98:
                if score < item.score:
                    print item.score
                    score = item.score
                    url = item.link
    if url == None:
        return {'ID':'Empty'}
    if score < 30:
        return {'ID':'Empty'}
    print url
    FirstSplitUrl = url.split("/comments/")
    SecondSplitUrl = FirstSplitUrl[1].split("/")
    SubmissionID = SecondSplitUrl[0]
    return {'ID':SubmissionID}


def Main():
    #print "Zoidberg"
    user_agent = 'Post Smart Comments see https://github.com/nikhil for the source'
    r = praw.Reddit(user_agent)
    o = OAuth2Util.OAuth2Util(r)
   
    mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
    client = MongoClient(mongoUrl)
    db = client.CheckList
    #o.refresh()
    user = r.get_redditor("Zoidberg333")
    gen = user.get_comments()
    for thing in gen:
        if thing.score <  0:
            thing.delete()

        
        
    lastids = []
    lastidlist = None
    if "LastIdList" not in db.collection_names():
        lastids = []
        lastidlist = {"value":lastids}
        db.LastIdList.insert_one(lastidlist)
    else:
        lastidCollection = db.LastIdList
        for listofids in lastidCollection.find():
            lastidlist = listofids
            lastids = lastidlist['value']
        
    
    if "RobotTimeStamp" not in db.collection_names():
        CurrentTime = {"value":datetime.datetime.now()}
        db.RobotTimeStamp.insert_one(CurrentTime)
        o.refresh()
        
       
    subreddit = r.get_subreddit('pics')
    for post in subreddit.get_hot(limit=100):
        for allTimeStamps in db.RobotTimeStamp.find():
            BeforeTimeTuple = time.mktime(allTimeStamps['value'].timetuple())
            CurrentTime = datetime.datetime.now()
            CurrentTimeTuple = time.mktime(CurrentTime.timetuple()) 
            TimeDiffrence = int(CurrentTimeTuple - BeforeTimeTuple) / 60
            print TimeDiffrence
            if TimeDiffrence >= 40:
                db.RobotTimeStamp.delete_one(allTimeStamps)
                o.refresh()
                CurrentTimeNow = {"value":datetime.datetime.now()}
                db.RobotTimeStamp.insert_one(CurrentTimeNow)
        postkey = str(vars(post)['id'])+str(vars(post)['created'])
        if postkey in lastids:
            continue
        lastids.append(postkey)

        url = urlparse(vars(post)['url'])
        imgurl = ''
        if url.netloc == 'imgur.com':
            if url.path.split('/')[1]=='a':
                continue
            else:
                imgurl = url.geturl()
            
        elif url.netloc == 'i.imgur.com':
            imgurl = url.geturl()
        if imgurl == '':
            continue

        value = CallKdapi(imgurl)
        SubmissionID = value['ID']
        print vars(post)['id']
        print "returned"
        print SubmissionID
        if SubmissionID == "Empty":
            continue
        
        nextlastid = vars(post)['id']
        duplicate = 0
        submission = r.get_submission(submission_id=SubmissionID)
        CommentList = submission.comments
        TopComment = CommentList[0].body
        submission2 = r.get_submission(submission_id=nextlastid)
        submission2.replace_more_comments(limit=16, threshold=10)
        flat_comments = praw.helpers.flatten_tree(submission2.comments)
        for comment in flat_comments:
            if comment.body == TopComment:
                duplicate = 1
        if duplicate == 1:
            continue
       
        try:
            post.add_comment(TopComment)
            post.upvote()
        except praw.errors.APIException as PrawError:
            lastids.remove(postkey)
            print PrawError
            break
        
        sg = sendgrid.SendGridClient('YourSendGridUserName', 'SendGridPass')
        RefLink = submission.permalink
        ThreadLink = post.permalink
        message = sendgrid.Mail()
        message.add_filter('templates', 'enable', '1')
        message.add_filter('templates', 'template_id', 'YourTemplateID')
        message.add_to('Nikhil Kumar <nikhilkumar516@gmail.com>')
        message.set_subject('Zoidberg333 made a comment')
        MessageHtmlStr = 'Dear Nikhil, <br> Zoidberg333 has just made a post: <br>' + TopComment + '<br> Here is a link to the thread: <br>' + ThreadLink + '<br> Here is the link to the reference: <br>' + RefLink
        message.set_html(MessageHtmlStr)
        message.set_text('')
        message.set_from('RedditBotWatch <BotWatch@kumarcode.com>')
        status, msg = sg.send(message)
        
        
        #SubmissionDict = {"HotLink":vars(post)['id'],"FromLink":SubmissionID}
        #requests.put("https://karmadecayapi-kumarcode.rhcloud.com/StoreSession/", timeout=connect_timeout, data=json.dumps(SubmissionDict))
        break

    db.LastIdList.delete_one(lastidlist)
    nextIdItem = {"value": lastids}
    db.LastIdList.insert_one(nextIdItem)
    InUseValue = {"value":1}
    db.InUse.delete_one(InUseValue)
    NotInUseValue = {"value":0}
    db.InUse.insert_one(NotInUseValue)


mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
client = MongoClient(mongoUrl)
db = client.CheckList


if "Zrunning" not in db.collection_names():
    RunningValue = {"value":1}
    db.Zrunning.insert_one(RunningValue)
else:
    RunCollection = db.Zrunning
    for RunElem in RunCollection.find():
        if RunElem['value'] == 1:
            print "Can't run"
            exit()
try:
    Main()
except:
    #e = sys.exc_info()
    #print "Error"
    #print e[0]
    #print e[1]
    #print e[2]
    RunCollection = db.Zrunning
    for RunElem in RunCollection.find():
        db.Zrunning.delete_one(RunElem)
        NewRunElem = {"value":0}
        db.Zrunning.insert_one(NewRunElem)
    traceback.print_exc()
    exit()

    

RunCollection = db.Zrunning
for RunElem in RunCollection.find():
    db.Zrunning.delete_one(RunElem)
    NewRunElem = {"value":0}
    db.Zrunning.insert_one(NewRunElem) 


