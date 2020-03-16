
class User:
    '''
        Class that represent needed parameters of a user
    '''

    def __init__(self, id, name, location, description, verified, followers, following, listed, favorites, status):
        '''
           parameters:
           verified: a boolean true or false
           followers: total number of followers
           following: total number of "followings"
           listed: total number of public lists that this user is a member of
           favorites: Total number of tweets this user has liked
           status: Total number of tweets (including retweets)
        '''
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.verified = verified
        self.followers = followers
        self.following = following
        self.listed = listed
        self.favorites = favorites
        self.status = status

    def __repr__(self):
        return 'User(id = {id},' \
               ' name = {name},' \
               ' location = {loc},' \
               ' description = {desc},' \
                ' followers = {followers},' \
                ' following = {following},' \
                ' listed = {listed},' \
                ' favorites = {fav},' \
                ' verified = {ver}'.format(
                    id=self.id,
                    name=self.name,
                    loc=self.location,
                    fav=self.favorites,
                    desc=self.description,
                    followers = self.followers,
                    following = self.following,
                    listed = self.listed,
                    ver = self.verified
                )

    # Comparison based on the user ID. 
    def __eq__(self, u):
        return self.id == u.id

    def __lt__(self, u):
        return self.id < u.id

    def __gt__(self, u):
        return self.id > u.id

    def __hash__(self):
        return self.id  

class Tweet:
    '''
        Class that represent needed parameters of a tweet
    '''

    def __init__(self, id, text, favorite, hashtags, media, retweet_count, urls, coordinates, created_at):
        '''
        Parameters:
        favorite: totaln number of favorite 
        hashtags: Array of strings containing all the hashtags
        media: Array of link to the media attached to the tweet
        url: array of links the tweet contains
        '''
        self.id = id
        self.text = text
        self.favorite = favorite
        self.hashtags = hashtags
        self.media = media
        self.retweet_count = retweet_count
        self.urls = urls
        self.coordinates = coordinates
        self.created_at = created_at

    def __repr__(self):
        return 'Tweet(id = {id},' \
               ' text = {text},' \
               ' created_at = {created_at},' \
               ' favorite_count = {fav},' \
               ' retweet_count = {ret},' \
                ' coordinates = {coor}'.format(
                    id=self.id,
                    text=self.text,
                    ret=self.retweet_count,
                    fav=self.favorite,
                    coor=self.coordinates,
                    created_at = self.created_at
                )

            
    # Comparison based on the tweet ID. the greater it is, the older the tweet is
    def __eq__(self, t):
        return self.id == t.id

    def __lt__(self, t):
        return self.id < t.id

    def __gt__(self, t):
        return self.id > t.id

    def __hash__(self):
        return self.id