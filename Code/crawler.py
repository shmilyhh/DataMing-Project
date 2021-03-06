import time
import requests
import json
from bs4 import BeautifulSoup
import json
import sys, os
from collections import OrderedDict
from datetime import date, timedelta, datetime
import codecs

class Crawler():
    def __init__(self, urls, folder):
        self.urls = urls
        self.results = []
        self.output_root = "../Data"
        self.folder = folder
        
        if not os.path.exists(self.output_root):
            os.makedirs(self.output_root)

    def get_page(self, url):
        try:
            headers  = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'}
            response = requests.get(url, headers = headers)
            if response.status_code == 403:
                print '403' + url
                sys.exit()
        
            return response.url, response.text
        except:
            print 'Error: ' + url
            return 'ERROR', 'ERROR'

    def parse_result(self, content):
        page = BeautifulSoup(content)
        d = {}

        # Keywords
        keywords = []
        # normal
        if page.find(attrs={"class":"keyword"}):
            if page.find(attrs={"class":"keyword"}).find_all(attrs={"class":"svKeywords"}):
                for kw in page.find(attrs={"class":"keyword"}).find_all(attrs={"class":"svKeywords"}):
                    keywords.append(kw.get_text())
        elif page.find(attrs={"class":"Keywords"}):
            if page.find(attrs={"class":"Keywords"}).find_all(attrs={"class":"keyword"}):
                for kw in page.find(attrs={"class":"Keywords"}).find_all(attrs={"class":"keyword"}):
                    keywords.append(kw.get_text())
        else:
            print "=================="
            print "not found keywords"
            print "=================="
        # Title
        if page.find("h1", "svTitle"):
            title = page.find("h1", "svTitle").get_text()
        else:
            title = 'None'
        # Abstract
        if page.find(id="spara0002"):
            abstract = page.find(id="spara0002").get_text()
        else:
            abstract = 'None'
        # Authors
        # authors = []
        # if page.find("ul", "authorGroup noCollab svAuthor").find_all("a", "authorName svAuthor"):
        #     for author in page.find("ul", "authorGroup noCollab svAuthor").find_all("a", "authorName svAuthor"):
        #         authors.append(author.get_text())

        d["keywords"] = keywords
        d["title"] = title
        d["abstract"] = abstract
        # d["authors"] = authors
                
        return d

    def crawler_paper(self):
        self.results = []
        i = 1
        
        for url in self.urls:
            final_url, content = self.get_page(url)

            print "Crawling ScienceDirect Data: ", url
            
            result = self.parse_result(content)
            if result["keywords"] == []:
                if not os.path.exists(os.path.join(self.output_root, 'content_no_keywords_'+self.folder)):
                    os.makedirs(os.path.join(self.output_root, 'content_no_keywords_'+self.folder))

                with codecs.open(os.path.join(self.output_root, 'content_no_keywords_'+self.folder,'science_direct_'+str(i)+'.html'), 'wb', 'utf-8') as out:
                    out.write(content)
            if result["abstract"] == []:
                if not os.path.exists(os.path.join(self.output_root, 'content_no_abstract_'+self.folder)):
                    os.makedirs(os.path.join(self.output_root, 'content_no_abstract_'+self.folder))

                with codecs.open(os.path.join(self.output_root, 'content_no_abstract_'+self.folder,'science_direct_'+str(i)+'.html'), 'wb', 'utf-8') as out:
                    out.write(content)
            if result["title"] == []:
                if not os.path.exists(os.path.join(self.output_root, 'content_no_title_'+self.folder)):
                    os.makedirs(os.path.join(self.output_root, 'content_no_title_'+self.folder))

                with codecs.open(os.path.join(self.output_root, 'content_no_title_'+self.folder,'science_direct_'+str(i)+'.html'), 'wb', 'utf-8') as out:
                    out.write(content)

            self.results.append(result)

            if not os.path.exists(os.path.join(self.output_root, 'results_'+self.folder)):
                os.makedirs(os.path.join(self.output_root, 'results_'+self.folder))

            with codecs.open(os.path.join(self.output_root, 'results_'+self.folder, 'paper_' + str(i) + '.json'), 'wb', 'utf-8') as f:
                    json.dump(self.results, f, indent=4)
            i += 1
            # time.sleep(5)

                
    def start_crawl(self):
        self.crawler_paper()

if __name__ == '__main__':
    data_path = "../Data"
    with open(os.path.join(data_path, "urls_IR.json")) as fp:
        ir = json.load(fp)
    with open(os.path.join(data_path, "urls_ML.json")) as fp:
        ml = json.load(fp)

    print("IR Crawlering...")
    Crawler(ir, "IR").start_crawl() 
    print("ML Crawlering...")
    Crawler(ml, "ML").start_crawl() 
    


