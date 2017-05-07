from archive import Crawler

link = 'https://twitter.com/kunalnayyar'
crawler = Crawler(link)

tweets = crawler.find_tweets()
keywords = crawler.do()

for tweet, keyword in zip(tweets, keywords):
	print ("Tweet : {} - Topics : {}".format(tweet, keyword))
	print ("\n")
