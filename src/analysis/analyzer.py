from __future__ import absolute_import, annotations
import json

import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()))

from src.models.twitter import User
from src.analysis.text_spacy import Spacytext

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
        media_count = 0
        for m in t.media:
            media_count += 1
            media[m['type']] = media.get(m['type'], 0) + 1 
        features['media'] = media
        features['media_count'] = media_count

        #URL features
        features['url_count'] = len(t.urls)

        return features

    def analyze_timeline(self, tweets):
        timeline_features = []
        for t in tweets:
            try:
                timeline_features.append(self.analyze_one(t))
            except ValueError:
                print(t.id)

        return timeline_features


if __name__ == '__main__':
    analyzer = Analyzer()

    with open("C:/Users/stefa/Desktop/U-Hopper/Datasets/DataExtractionDatasetGenerator/dataset.json") as in_file:
        data = json.load(in_file)

    total = []
    for u in data[:1]:
        user = User.from_repr(u)
        u['timeline'] = analyzer.analyze_timeline(user.timeline)

        total.append(u)
        
    total_json = json.dumps(total, indent=4)

    with open('test_analyzed.json', 'w') as out:
        out.write(total_json)
    
    #Open the dataset
