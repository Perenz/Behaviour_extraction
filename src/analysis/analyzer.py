from __future__ import absolute_import, annotations
from analysis.text_spacy import Spacytext

class Analyzer:
    #Could use a parameter to set the features type
    def __init__(self):
        self.spacy_text = Spacytext()

    def analyze_one(self, t):
        data_text = t.text
        features = {}
        #Copy features from tweet
        features = t.to_features()
        
        #Text features
        features['text_features'] = self.spacy_text.analyze(data_text)
       
       #Media features
        media = {}
        for m in t.media:
            media[m['type']] = media.get(m['type'], 0) + 1 
        features['media'] = media

        #URL features
        features['url_count'] = len(t.urls)

        return features

    def analyze_timeline(self, tweets):
        timeline_features = []
        for t in tweets:
            timeline_features.append(self.analyze_one(t))

        return timeline_features