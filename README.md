#IRedditBefore
Automated commenting on <a href="https://www.reddit.com" alt="Reddit">Reddit</a> reposted threads using <a href="http://karmadecay.com/" alt="Karma Decay">Karma Decay</a>.<br>The bot process works as follows: <br>
<ol>
<li> Looks for rising reposted links on Reddit (<a href="https://www.reddit.com/r/funny/" alt="r/funny">r/funny</a>) </li>
<li> Aquires all source/reposted threads of that submission </li>
<li> Takes the top thread and copys the top comment </li>
<li> Posts comment on current reposted thread </li>
<li> Sends user an email about the comment </li>
</ol>
####Example 1
<img src="Example1.png" alt="Example1">
####Example 2
<img src="Example2.png" alt="Example2">
####Example 3 
Just after I deleted the bot
<hr>
<img src="Example3.png" alt="Example3">

###Why???
This was primarily an experimental project. I wanted to see how Reddit would react to reposted comments. The bot recieved 25k comment karma in 3 days. After 3 days I deleted the bot. 

###Email Example
<img src="Email.png" alt="Email">

###Working with Karma Decay
I used kdapi as the base for my Karma Decay script. I fixed many issues with the webpage parsing. Karma Decay also blocked many US AWS ips, so I used a proxy.

###How to use this without Openshift?
I have a cron script in .openshift/cron/minutely called CheckMyList. You need to set up a cron so that Zoidberg333.py runs every minute. You can rename the script to your reddit username.You will also need to setup a mongodb server. Then whenever you see "os.environ['OPENSHIFT_MONGODB_DB_URL']" you need to enter the url to your mongodb server. Also you will need to setup your account for Oauthentication. You would need to modify oauthappinfo.txt. The guide to oauth2 is <a href="here:https://github.com/reddit/reddit/wiki/OAuth2" alt="OAuth2">here</a>. Basically you need two values the application id which is the hash just below the script title and the secret which is in the field labeled secret. Applicaiton id goes on the first line and secret goes on the second line. It should ask you to authenticate the first time you run Zoidberg333.py.You also need sendgrid for the emails, but you can comment lines 146-158 if you want to. 

###Resources Used
- <a href="https://github.com/ethanhjennings/karmadecay-api" alt="kdapi">kdapi</a>
- <a href="https://github.com/SmBe19/praw-OAuth2Util" alt="praw-OAuth2Util">praw-OAuth2Util</a>
- <a href="https://www.openshift.com/" alt="openshift">openshift</a>

