### Authors: Khoa Vo, Than Phan, Aaron Sanders


__spec:__ 
``` 
Python 3 or above
__Packages:__
Json
Tornado
Elasticsearch
Lucene
```


__The following command lines are for installing the packages:__
```
pip install tweepy
pip install tornado
pip install simplejson
msiexec.exe /i elasticsearch-6.6.2.msi /qn
```

__Installation process for elasticsearch (for mac user)__
```
brew install elasticsearch
python3 -m pip install elasticsearch
```

Other option is to download lucene from their [website here](https://lucene.apache.org/core/2_9_4/demo.html).


__Source codes:__
```
*templates
  -listTemplate.html
  -searchInput.html
*.DS_store
*crawler.sh
*es.py
*query.py
*searchApp.py
*tweet.json
*tweets.py
*README.md
```

__Link it Crawled Data (Too Big for Github Push and Large File Extension Not Cooperating__
[1 gb of tweets](https://drive.google.com/drive/folders/1VwIa-oE8e6SWdFsaZISS0w1meiDyBbkq?usp=sharing)

__Tweepy Crawler Design:__
Using the tweepy Python library and assigned Twitter developer API keys, we crawl Twitter using a popular seed account with millions of followers (i.e. Twitter, or CNN). Since the seed account has a sizeable list of followers with probable random geological distribution, we iterate through the seed’s followers list, extracting a pre-defined number of tweets from each user’s timeline. This value, as well as the seed Twitter account, is defined via command line arguments when deploying the crawler with the shell script provided. Periodically the crawler outputs the size of the output data file being created. The user must Ctrl-C when desired file size met, in our case ~1.2 gigabytes.

Crawler utilizes Tweepy cursors to easily access a user’s timeline among other Twitter user attributes. Each tweet structure has an implicit _json function that returns an encapsulating json object, which is then dumped to “tweets.json” output file in the specified output path directory, also stated in the command line argument. Tweets are collected into a list object up unto a list size of 1000 before writing the tweets to file and flushing. The now full list is emptied and refilled until completion. Each tweet._json is output to a single line, separated by a newline. Additionally, we flush whenever the twitter rate limit is reached, which halts the crawler for ~800 seconds each time. As a result, it took roughly 18-24 hours to crawl 1 gig of data. We keep track of each visited user so not to grab tweets from any one user more than once.

__Crawler Limitations:__
Twitter enforces a rate limit on its access to it’s data, so crawling time is drastically delayed, being forced to wait for approximately 13 minutes every 2 to 3 minutes of crawling. 


__Deploying Tweet (Tweepy) crawler:__
```
./crawler [seed Twitter user/screen name] [num of tweets to collect from seed's followers list] [output directory path]
```
For instance, to crawl the account for the movie studio A24 at 50 tweets per user...
```
./crawler a24 50 ./output_folder
```
Crawler periodically prints out the generated output file size so that user can cntrl-C to halt crawling when desired volume met.


__Run elsaticsearch instruction:__

Go to elasticsearch directory and run elasticsearch on your computer.
Locate elasticsearch directory by
```
brew info elasticsearch
```
Go to elasticsearch directory and run it
```
./elasticsearch
```
Set up index
```
python3 es.py
```
query.py is use to retrieve relevant documents.

__Web Interface:__

After runing the source codes, open a web browers and open the following URL:
[http://localhost:8888/](http://localhost:8888/)
```
You will see a search box where you can enter a query to find relevant tweets in regards to your query.
Once you press enter or search, you will be transfered to the results page that contains the top 10 results.
```
