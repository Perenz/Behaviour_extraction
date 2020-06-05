import re
import it_core_news_sm
from spacymoji import Emoji
from collections import Counter

def hashtag_pipe(doc):
    merged_hashtag = False
    while True:

      for token_index, token in enumerate(doc):
        #When a new token composed only by # is found
        if token.text == '#':
          end_index = token_index+1 
          #Check if next token is legal
          if end_index < doc.__len__():
            with doc.retokenize() as retokenizer:
              #Merge the token with # and the next one
              attr = {"LEMMA": '#'+doc[end_index].lemma_, "POS": doc[end_index].pos_, "TAG":doc[end_index].tag_}
              retokenizer.merge(doc[token_index:token_index+2], attrs=attr)
              #token_index:token_index+len(doc[end_index])
            merged_hashtag = True
            break
     
      if not merged_hashtag:
        break
      merged_hashtag=False

    return doc

class Spacytext:
    def __init__(self):
        self.nlp = it_core_news_sm.load()
        emoji = Emoji(self.nlp)
        sentencizer = self.nlp.create_pipe("sentencizer")

        #Add components to the pipeline
        self.nlp.add_pipe(emoji, first=True)
        self.nlp.add_pipe(hashtag_pipe, first=True)
        self.nlp.add_pipe(sentencizer)

    def analyze(self, text):
        '''
            Given a text, return a document of the analyzed text.
            Analysis comprehends tokenization, lemmatization and POS tagging.
        '''
        #Remove $URL$
        text = text.replace('$URL$', '')

        features = {}
        #Count capital letters
        features['num_capital'] = sum(1 for char in text if char.isupper())

        #Norm whitespaces and lower
        NORM_WHITESPACE = re.compile(r"\s+")
        text = NORM_WHITESPACE.sub(" ", text).strip().lower()

        #Run the pipeline
        tok_doc = self.nlp(text)

        #Build the features of the analysis
        #TODO Should normalise to tweet limit? (140/280)
        
        features['sentence_num'] = len(list(tok_doc.sents))  #Number of sentences
        if features['sentence_num'] == 0:
          features['sentence_num'] = 1
        features['word_num'] = len(tok_doc) #Number of words
        if features['word_num'] == 0:
          features['word_num'] = 1
        features['char_num'] = sum(len(t.text) for t in tok_doc) #Number of chars
        features['word_per_sentence'] = features['word_num'] / features['sentence_num'] #Words per sentence
        features['char_per_sentence'] = features['char_num'] / features['sentence_num'] #Chars per sentence
        features['char_per_word'] = features['char_num'] / features['word_num'] #Chars per word

        stop_word= []
        words = []
        emoji = []
        pos_tag = []
        punct = ''
        for t in tok_doc:
            #POS tag
            pos_tag.append(t.pos_)
            #filter type
            if t.is_stop:
                stop_word.append(t.lemma_)
            elif t.is_punct:
                punct = punct + t.lemma_
            elif t._.is_emoji:
                emoji.append(t.lemma_)
            else:
                words.append(t.lemma_)

        #From punct token, count the exact number
        punct = {c:val for c, val in Counter(punct).items() if c in '.,!?-()[\]'}
    

        features['words'] = dict(Counter(words).most_common())
        features['stopwords'] = dict(Counter(stop_word).most_common())
        features['punct'] = punct
        features['emojis'] = dict(Counter(emoji).most_common())
        features['pos_tag'] = dict(Counter(pos_tag).most_common())

        return features