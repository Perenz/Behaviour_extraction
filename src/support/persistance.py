import json
from pymongo import MongoClient

'''
def check_user_last(id):
    
    #1093586351549804544
    ids = [1, 2, 3, 1093586351549804544]
    print("Checking")
    if int(id) in ids:
        with open('profile.json') as f:
            data = json.load(f)
        last = data.get('last')
        print(last)
        return last
    else:
        return None
'''

class mongoDBDao:
    def __init__(self):
        #Initialize mongo connection
        self.client = MongoClient(host='localhost', port=27017)
        self.db = self.client['pymongo_intern']
        self.users = self.db.users #users collection

    def get_user(self, id):
        return self.users.find_one({'_id': id})

    def get_user_last(self,id):
        user = self.get_user(id) 
        if user is not None:
            return user.get('last')
        else:
            return None

    def insert_user_last(self, id, last=None):
        #Check if passed last is bigger than stored one
        stored_last = self.get_user_last(id)
        if last is not None:
            data = {'$set':{'last':last}}
            self.users.update_one({"_id": id}, data, upsert=True)

    

        