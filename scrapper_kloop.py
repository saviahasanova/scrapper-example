
# coding: utf-8

# In[282]:


import pandas as pd
import re
import requests
from lxml import html
import sys


# In[283]:


class Scrapper:
    
    def __init__(self, source, link_pattern, xpath, df, max_while = 4, max_links = 20):
        self.source = source
        self.link_pattern = link_pattern
        self.xpath = xpath
        self.df = df
        self.max_while = max_while
        self.max_links = max_links
        self.link_storage = []
        self.link_history = []
    
    def scrape(self, seed_link):
        self.link_storage.append(seed_link)
        print('Put link into seed link storage')
        i = 0
        while True:
            links_list_length = len(self.link_storage)
            print('Entered while cycle')
            links = self.link_storage.copy()
            for link in links:
                print('Entered for cycle')
                if link not in self.link_history:
                    seed_page = self.load(link)
                    print('Tried to load: ' + link)
                    self.link_history.append(link)
                    if seed_page:
                        print('Loaded: ' + link)
                        if self.is_needed(link):
                            print('Link is needed: ' + link)
                            self.extract_info(seed_page)
                            print('Info extracted')
                        self.extract_links(seed_page)
                        print('Links extracted')
                if self.df.shape[0] > self.max_links:
                    break
            if links_list_length == len(self.link_storage):
                i += 1
            if self.df.shape[0] > self.max_links or i > self.max_while:
                break
        #    self.scrape(self.link_storage)
        return self.df
        
    
    def extract_links(self, page):
        pattern = self.source + '[a-z0-9\-\_\.\/]+'
        links = re.findall(pattern, page.text)
        for link in links:
            if not link in self.link_storage:
                self.link_storage.append(link)
    
    def load(self, link):
        response = requests.get(link)            
        return response
    
    def extract_info(self, page):
        tree = html.fromstring(page.content.decode('UTF-8'))
        result = tree.xpath(self.xpath)
        self.df = self.df.append(pd.DataFrame(result, columns=list(self.df.columns)), ignore_index=True)
        return result
    
    def is_needed(self, link):
        return bool(re.search(self.link_pattern, link))


# In[284]:


df = pd.DataFrame(columns=['title'])

scrapper_kloop = Scrapper('https://www.bbc.co.uk/news/world', 
                          '/news/world',
                          '//h1/text()',
                          df)


# In[285]:


scrapper_kloop.scrape('https://www.bbc.com/news/world-middle-east-46067959https://www.bbc.co.uk/news/world-europe-46049204')


# In[237]:


page = scrapper_kloop.load('https://www.bbc.com/news/world-middle-east-46067959')


# In[240]:


info = scrapper_kloop.extract_info(page)


# In[261]:


scrapper_kloop.df

