from pymongo import MongoClient
import os

mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
client = MongoClient(mongoUrl)
db = client.CheckList
db.Zrunning.drop()
db.Crunning.drop()
db.RobotTimeStamp.drop()
db.BenderTimeStamp.drop()


