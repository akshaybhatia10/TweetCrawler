#import time
###--- IMPORTING DEPENDENCIES ---###
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from rake_nltk import Rake

###--- USING SELENIUM DRIVER TO SCROLL TO END OF WEBPAGE ---###
# driver = webdriver.Chrome()
# driver.get(link)

# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)

###--- MAIN CLASS CRAWLER ---###
###--- @PARAMS LINK: THE TWITTER HANDLE  ---###
class Crawler:
    
    def __init__(self, link):
        self.link = link

    ###--- RETURNS LIST OF FIRST 20 TWEETS ---###
    def find_tweets(self):
        response = urllib2.urlopen(self.link)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        i = 1
        tweet_list = []
        for tweets in soup.find_all('div', {'class':'tweet'}):
            if i <=20:
                raw = tweets.find('p', {'class': 'tweet-text'}).text.encode('ascii', 'ignore')
                tweet_list.append(raw)
            i = i + 1
        
        return tweet_list

    ###--- RETURNS LIST OF TWEETS WITH STOP WORDS REMOVED ---###    
    def preprocess(self, tweet):
    #     tweet = tweet.lower()
    #     tweet = " ".join(tweet.split('#'))
    #     tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #     tweet = re.sub('((www\.[^\s]+)|(https://[^\s]+))','URL',tweet)
    #     tweet = re.sub("http\S+", "URL", tweet)
    #     tweet = re.sub("https\S+", "URL", tweet)
    #     tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #     tweet = tweet.replace("AT_USER","")
    #     tweet = tweet.replace("URL","")
    #     tweet = tweet.replace(".","")
    #     tweet = tweet.replace('\"',"")
    #     tweet = tweet.replace('&amp',"")
    #     tweet  = " ".join([word for word in tweet.split(" ") if re.search('^[a-z]+$', word)])
    #     tweet = re.sub('[\s]+', ' ', tweet)
    #     tweet = tweet.strip('\'"')
    #     return tweet
        tweet = ''.join(i for i in tweet if not i.isdigit())
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", tweet).split())  
        return tweet

    ###--- RETURNS ALL THE KEYWORDS ---###    
    def get_keywords(self):
        r = Rake()
        keyword = []
        tweet_list = self.find_tweets()  
        for tweet in (tweet_list):
            normalized_tweet = self.preprocess(tweet)
            r.extract_keywords_from_text(normalized_tweet)
            keyword.append(r.get_ranked_phrases())
        return keyword

    ###--- RETURNS THE TOPICS RELEVANT TO THE TWEET ---###    
    def do(self):
        final_topics = []
        tweets = self.get_keywords()
        for tweet in (tweets):
            n = []
            if len(tweet) == 0:
                continue
            else:
                for word in (tweet):
                    x = word.split(" ")
                    for topic in x:
                        if len(topic) > 5:
                            n.append(topic)
                final_topics.append(n)    

        return final_topics            
       