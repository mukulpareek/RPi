#!/usr/bin/env python
# coding: utf-8

# # Web scraping RSS and Topic Models

# In[1]:

try:
    

    import newspaper
    import feedparser
    import numpy as np
    import pandas as pd
    import requests
    import datetime 
    from tqdm import tqdm
    import nltk
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import NMF, LatentDirichletAllocation
    import joblib


    # ## Web Scraping

    # In[2]:


    # Blank dataframe, based on fields identified later

    rss_feeds = pd.DataFrame(columns = ['title',  'summary',  'links',  'link',  'id',  'guidislink',  'published',  
                                        'published_parsed',  'title_detail.type',  'title_detail.language',  
                                        'title_detail.base',  'title_detail.value',  'summary_detail.type',  
                                        'summary_detail.language',  'summary_detail.base',  'summary_detail.value',  
                                        'media_content',  'feedburner_origlink'])


    # In[3]:


    # List of RSS URLs to scrape

    rss_urls = [r'http://www.schneier.com/blog/index.rdf', 
                r'http://feeds.feedburner.com/darknethackers', 
                r'http://securityaffairs.co/wordpress/feed', 
                r'http://healthitsecurity.com/feed/', 
                r'http://seanmason.com/feed/', 
                r'http://threatpost.com/feed', 
                r'http://feeds.trendmicro.com/Anti-MalwareBlog/', 
                r'http://www.infosecurity-magazine.com/rss/news/', 
                r'http://krebsonsecurity.com/feed/', 
                r'http://www.darkreading.com/rss/all.xml', 
                r'http://blog.kaspersky.com/feed/', 
                r'http://www.baesystems.com/page/rss?lg=en', 
                r'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml', 
                r'http://feeds.feedburner.com/scmagazinenews', 
                r'http://taosecurity.blogspot.com/atom.xml', 
                r'http://www.rms.com/blog/feed/', 
                r'http://iscxml.sans.org/rssfeed.xml', 
                r'https://community.qualys.com/blogs/securitylabs/feeds/posts', 
                r'http://googleonlinesecurity.blogspot.com/atom.xml', 
                r'http://thehackernews.com/feeds/posts/default', 
                r'http://www.us-cert.gov/current/index.rdf', 
                r'http://feeds.feedburner.com/Securityweek', 
                r'http://nakedsecurity.sophos.com/feed/', 
                r'http://feeds.arstechnica.com/arstechnica/index/', 
                r'http://www.csoonline.com/feed/attribute/41014', 
                r'http://blogs.rsa.com/feed/', 
                r'http://feeds.feedburner.com/Techcrunch', 
                r'http://recode.net/feed/', 
                r'http://www.techmeme.com/index.xml', 
                r'http://www.technologyreview.com/stream/rss/']


    # In[4]:


    # Get all the feed entries.  But the dataframe resulting from this has only a summary line, 
    # not the entire text of the article.  For that we will pull the URL in using the 
    # newspaper library later.
    print('\nPulling articles from RSS URLs...')

    for rss in tqdm(rss_urls):
        try:
            feed = feedparser.parse(rss)
            rss_feeds=pd.concat([rss_feeds, pd.json_normalize(feed.entries)], axis=0)
        except:
            print('Error with ',rss)
    print(len(rss_feeds), 'items in rss_feed dataframe')    

    # In[5]:


    # Remove duplicate URLs

    urllist =rss_feeds.link.unique()


    # In[6]:


    # Get full text using scraping from the newspaper library

    from newspaper import Article
    import pandas as pd
    df = pd.DataFrame(columns = ["date",  "URL", "authors", "keywords", "summary", "text"])
    print('\nPulling text from URLs identified earlier...')
    for url in tqdm(urllist):
        article = Article(url)
        try:
            article.download()
            article.parse()
            article.nlp()
            dict1 = {"date": article.publish_date, "URL": url, "authors": article.authors,              "keywords": article.keywords, "summary": article.summary, "text": article.text}
        #print(dict1)
            df = df.append(dict1, ignore_index=True)
        except:
            print('Something wrong with', url)

    print(len(df),'stories in dataframe df')




    # In[7]:


    # Merge the RSS dataframe with the full text obtained from the 
    # newspaper library

    final = rss_feeds.merge(df,how="right", left_on="link", right_on="URL")
    print(len(final),'unique articles in file.')


    # In[8]:


    # Save the file
    final.to_pickle(r'/home/pi/security_data/' + 'securitynews_' + datetime.datetime.now().strftime("date_%Y.%m.%d_time_%H.%M") + '.pkl', protocol=4)
    print('Pickle file created')

except:
    
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content('This is my message')

    msg['Subject'] = 'Security Data Script Failed'
    msg['From'] = "Script Fail <email_here@gmail.com>"
    msg['To'] = "Mukul <mp@pareek.org>, Work <mukul.pareek@wellsfargo.com>"
    msg['Cc'] = "pareekhome@gmail.com"

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("email_here@gmail.com", "password_here")
    server.send_message(msg)
    server.quit()
