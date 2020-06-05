from __future__ import absolute_import, annotations
from twitter.api import TweepyAPI, User
from support.persistance import mongoDBDao
from analysis.analyzer import Analyzer
from aggregate.main import Aggregator
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

def get_user(UserID):
#Open DB connection
    conn = mongoDBDao()

    #Check persistance and get last
    last = conn.get_user_last(UserID)

    twApi = TweepyAPI()
    user=twApi.get_user(UserID)
    #DEBUG
    user.add_tweets(twApi.get_user_timeline(UserID, since=None))

    #Update last
    conn.insert_user_last(UserID, user.last)

    #Get user representation and return
    return user

@app.route('/profile', methods=['GET'])
def twitter_profile():
    UserID = int(request.args.get('id'))
    if UserID is not None:
        res = get_user(int(UserID))
        return jsonify(res.to_repr())
    else:
        raise errorHandler('Invalid id parameter', statusCode=404)

@app.route('/analyze', methods=['GET'])
def analyze():
    UserID = request.args.get('id')
    if UserID is not None:
        analyzer = Analyzer()
        user = get_user(int(UserID))
        res = user.to_repr()
        #Modify timeline with the featured tweets
        res['timeline'] = analyzer.analyze_timeline(user.timeline)
        return jsonify(res)
    else:
        raise errorHandler('Invalid id parameter', statusCode=404)

@app.route('/aggregate', methods=['GET'])
def aggregate():
    UserID = request.args.get('id')
    if UserID is not None:
        analyzer = Analyzer()
        user = get_user(int(UserID))
        res = user.to_repr()
        #Modify timeline with the featured tweets
        res['timeline'] = analyzer.analyze_timeline(user.timeline)
        
        #Aggreagates
        aggregator = Aggregator()
        batch = aggregator.aggregates(res)
        
        return jsonify(batch)
        #return jsonify(res)
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
