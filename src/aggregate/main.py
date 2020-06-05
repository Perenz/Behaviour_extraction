from datetime import datetime
from collections import Counter
import sys
import json

class Aggregator:
    
    '''
        Input: analyzed user
        Output: Aggregated user
    '''

    def __init__(self):
        pass

    def aggregates(self, user):
        batch = {}

        #Iterate the timeline and put together the features
        tweets_in_day = [0 for i in range(24)]
        tweets_num = user['tweets_number']
        legal_tweets_num = 0

        #Days covered by the first and last tweet
        days = (datetime.strptime(user['timeline'][0]['created_at'], "%d/%m/%Y, %H:%M:%S")) - (datetime.strptime(user['timeline'][-1]['created_at'], "%d/%m/%Y, %H:%M:%S"))
        delta_days = days.days if days.days != 0 else 1
        tweets_per_day = tweets_num/delta_days
        #print(days.days)

        #User location
        #0 there is no location, 1 there is
        has_loc = 0 if user['location'] == '' else 1

        #Init tweet type
        tweets_type = [0 for i in range(4)]

        words = Counter()
        stop_words = Counter()
        emoji = Counter()
        pos_tag = Counter()
        hashtags = Counter()
        punct = Counter()
        media = Counter()
        fav_min = ret_min = sys.maxsize 
        fav_max = fav_avg = ret_max = ret_avg = 0 
        url_count = mention_count = 0
        followers = user['followers']

        total_token = 0


        char_num = char_per_sentence = char_per_word = 0
        sentence_num = word_num = word_per_sentence = 0

        hashtag_count = media_count = 0
        punct_num=0

        for t in user['timeline']:
            #Count tweet types
            tweets_type[t['tweet_type']] += 1/tweets_num

            #Tweet in 24 hours
            datetime_obj = datetime.strptime(t['created_at'], "%d/%m/%Y, %H:%M:%S")
            tweets_in_day[datetime_obj.hour] += 1/tweets_num


            if t['tweet_type'] != 2:
                #Count number of "legal" tweets
                legal_tweets_num += 1
                #Text features
                #Words frequencies at user level: Sum all the features and then divide by number of total words
                total_token += t['text_features']['word_num']
                words += Counter(t['text_features']['words'])
                stop_words += Counter(t['text_features']['stopwords'])
                emoji += Counter(t['text_features']['emojis'])
                punct_counter = Counter(t['text_features']['punct'])
                punct += punct_counter
                pos_tag += Counter(t['text_features']['pos_tag'])

                punct_num += sum(punct_counter.values())
                

                #hashtag, url, media and mentions
                #Avg per tweet, total singular count for hashtags and mentions(?)
                hashtags += Counter([h.lower() for h in t['hashtags']])
                hashtag_count += len(t['hashtags'])
                media += Counter(t['media'])
                media_count += t['media_count']
                url_count += t['url_count']
                mention_count += len(t['mentions'])

                #AVG char_num, ... / Num of valid tweets
                char_num += t['text_features']['char_num']
                char_per_sentence += t['text_features']['char_per_sentence']
                char_per_word += t['text_features']['char_per_word']
                sentence_num += t['text_features']['sentence_num']
                word_num += t['text_features']['word_num']
                word_per_sentence += t['text_features']['word_per_sentence']
                

                #AVG, Max and Min favourite_count and retweet_count normalized per followers number
                fav_min, fav_max = min(fav_min, t['favourite_count']), max(fav_max, t['favourite_count'])
                fav_avg += t['favourite_count']

                ret_min, ret_max = min(ret_min, t['retweet_count']), max(ret_max, t['retweet_count'])
                ret_avg += t['retweet_count']

        #Also print user ID,


        '''
        print({k:v/total_token for k,v in words.items()})
        #print(dict(words))
        print({k:v/total_token for k,v in stop_words.items()})
        print({k:v/total_token for k,v in emoji.items()})
        print({k:v/total_token for k,v in pos_tag.items()})
        print({k:v/total_token for k,v in punct.items()})
        print(hashtag_count)
        print(tweets_per_day)
        print(tweets_in_day)
        print(tweets_type)
        print(fav_min/followers, fav_max/followers, fav_avg/legal_tweets_num/followers)
        print(ret_min/followers, ret_max/followers, ret_avg/legal_tweets_num/followers)
        '''

        #mbti and gender in dEBUG
        keys = ['id', 'followers', 'following', 'last', 'listed', 'location']
        batch = {k:user[k] for k in keys}

        batch['follower_ratio'] = user['followers']/user['following'] if user['following'] != 0 else user['followers']
        batch['tweet_count'] = tweets_num
        batch['legal_tweet_count'] = legal_tweets_num

        batch['has_loc'] = has_loc
        batch['tweet_per_day'] = tweets_per_day
        batch['tweet_per_24'] = tweets_in_day
        batch['tweet_type'] = tweets_type

        #batch

        batch['word_num'] = word_num/legal_tweets_num
        batch['sentence_num'] = sentence_num/legal_tweets_num
        batch['char_num'] = char_num/legal_tweets_num
        batch['word_per_sentence'] = word_per_sentence/legal_tweets_num
        batch['char_per_word'] = char_per_word/legal_tweets_num
        batch['char_per_sentence'] = char_per_sentence/legal_tweets_num

        batch['hashtag_per_tweet'] = hashtag_count/legal_tweets_num
        batch['hashtags'] = {k:v/hashtag_count for k,v in hashtags.items()}
        batch['media_per_tweet'] = media_count/legal_tweets_num
        batch['media'] = {k:v/media_count for k,v in media.items()}
        batch['url_per_tweet'] = url_count/legal_tweets_num
        batch['mention_per_tweet'] = mention_count/legal_tweets_num

        batch['words'] = {k:v/total_token for k,v in words.items()}
        batch['stop_words'] = {k:v/total_token for k,v in stop_words.items()}
        batch['emoji'] = {k:v/total_token for k,v in emoji.items()}
        batch['pos_tag'] = {k:v/total_token for k,v in pos_tag.items()}
        batch['punct'] = {k:v/total_token for k,v in punct.items()}
        batch['punct_num'] = punct_num/legal_tweets_num

        


        return batch



if __name__ == '__main__':
    aggregator = Aggregator()


    with open("C:/Users/stefa/Desktop/U-Hopper/UHopperCodeTests/dataset_analyzed.json") as in_file:
        data = json.load(in_file)

    total = []
    for u in data:
        user = aggregator.aggregates(u)

        total.append(user)
        
    total_json = json.dumps(total, indent=4)

    with open('dataset_aggregated.json', 'w') as out:
        out.write(total_json)
    
    #Open the dataset