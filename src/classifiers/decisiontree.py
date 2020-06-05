from __future__ import absolute_import
from __future__ import annotations

import json
from sklearn import tree

class SimpleDecisionTree:

    def __init__(self, atype):
        '''
        Instantiate a new decision tree
        :type: the aspect this specific classifier predict
        '''
        self.clf = tree.DecisionTreeClassifier()
        self.atype = atype

    def fit(self):
        '''
            Train the classifier of "type" specified
        '''

        '''
        type: 
            0 E/I
            1 S/N
            2 T/F
            3 J/P
        '''
        labels = {0: 'E', 1: 'S', 2: 'T', 3:'J'}
        label = labels[self.atype]
        #Open the dataset
        with open("dataset_aggregated", 'r') as in_file:
            data = json.load(in_file)

        #Select the features
        #'tweet_per_day', 'tweet_per_24', 'tweet_type', 'media', 'punct_num'
        keys = ['followers', 'following', 'listed', 'follower_ratio', 'has_loc', 'word_num', 'sentence_num', 'char_num', 'word_per_sentence', 'char_per_word', 'char_per_sentence', 'hashtag_per_tweet', 'media_per_tweet', 'url_per_tweet', 'mention_per_tweet']
        set_X = []
        set_y = []
        for u in data:
            set_X.append([u[k] for k in keys])
            #Check mbti field
            mbti = u['mbti']

            set_y.append([0 if mbti[self.atype]==label else 1])

        self.tree.fit(set_X, set_y)

    
    def predict(self, profile):
        keys = ['followers', 'following', 'listed', 'follower_ratio', 'has_loc', 'word_num', 'sentence_num', 'char_num', 'word_per_sentence', 'char_per_word', 'char_per_sentence', 'hashtag_per_tweet', 'media_per_tweet', 'url_per_tweet', 'mention_per_tweet']
        set_X = [profile[k] for k in keys]

        return self.tree.predict(set_X)[0]


    
class SimpleEIDecisionTree(SimpleDecisionTree):
    '''
    Decision Tree for Extrovert/Introvert
    '''
    atype = 0

    def __init__(self):
        super().__init__(atype)

        