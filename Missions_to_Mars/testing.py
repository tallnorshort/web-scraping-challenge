import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Dumpster_DB"]

use Dumpster_DB