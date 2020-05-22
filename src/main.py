from __future__ import absolute_import, annotations
from twitter.api import TweepyAPI
from models.twitter import User
from support.persistance import check_user_last
import json

from flask import Flask, request, jsonify
app = Flask(__name__)
app.config['DEBUG'] = True

class errorHandler(Exception):
    def __init__(self, message, statusCode = None):
        self.message = message
        if statusCode is not None:
            self.status_code = statusCode

    def to_dict(self):
        '''
            Return the error messagge in a json format
        '''
        return {'Code':self.status_code, 'Message':self.message}

@app.route('/')
def welcome():
    return "Welcome!"

@app.route('/profile', methods=['GET'])
def twitter_profile():
    UserID = request.args.get('id')
    if UserID is not None:
        #Check persistance
        last = check_user_last(UserID)

        twApi = TweepyAPI()
        user=twApi.get_user(UserID)
        user.add_tweets(twApi.get_user_timeline(UserID, since=last))

        #Get user representation and return
        res=user.to_repr()
        return jsonify(res)
    else:
        raise errorHandler('Invalid id parameter', statusCode=404)
    

if __name__ == '__main__':
    #Default host = 127.0.0.1
    #Default port = 5000
    app.run()

'''
twApi = TweepyAPI()
#Stefano Perenzoni
UserID = 1093586351549804544



#print(user)
#print(data)

#IDs already in the system
ids = [1, 2, 3, 1093586351549804544]

#Check if User was already dowloaded
if UserID in ids:
    with open('profile.json') as f:
        data = json.load(f)
    old = twApi.user_from_repr(data)
    
    #Download the updated user and add new activities
    user = twApi.get_user(UserID)
    user.add_tweets(twApi.get_user_timeline(UserID, since=old.last))
    #print(user)
else:
    #Download the user and then his activities
    user=twApi.get_user(UserID)
    user.add_tweets(twApi.get_user_timeline(UserID))
    #print(user)


res=user.to_repr()
res_json= json.dumps(res, indent=4)
print(res_json)

'''
'''
res = user.to_repr()
print(res)
res_json = json.dumps(res, indent=4, ensure_ascii=False)
with open("prova.json", 'w') as f:
    f.write(res_json)

with open("prova.json", "r") as in_f:
    data = json.load(in_f)
    #print(data)
'''
