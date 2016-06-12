#encoding:utf-8
"""
follow all the linked text in the home page of news sites
1. do some filtering with the links
2. check for repeat links
"""

import os
import glob
import sys
import datetime
import re
import codecs
import pdb
import json
from bs4 import BeautifulSoup
import pdb

# gpf newsParser
from newsParser import newsParser
from wgetCrawl import wgetCrawl
from rssParser import rssParser 

curfilepath = os.path.realpath('__file__')
curfolderpath = os.path.dirname(curfilepath)
#debug
print 'curfolder path:',curfolderpath


# append current folder to system path
sys.path.append(curfolderpath)
def crawl_sina_rss():
    wgg = wgetCrawl()
    # title_content info
    rss_category = dict()
    xmlfilepath = os.path.join(curfolderpath,'sina_all_opml.xml')
    with codecs.open(xmlfilepath,'r','utf8') as fin:
        psr = newsParser(fin)
        # list of title & urls
        title,contenturl = psr.parse_sina_xml()
    title = map(lambda x:x.encode('utf8'),title)
    contenturl = map(lambda x:x.encode('utf8'),contenturl)
    zip_title_url_list = zip(title,contenturl)
    for curtitle,cururl in zip_title_url_list:
        rss_category[curtitle] = dict(url=cururl)
    rssnewsfolder = os.path.join(curfolderpath,'sina_news')
    # craw each content url
    cID = 1
    for curtitle,urlitem in zip_title_url_list:
        outputhtmlfilename = os.path.join(rssnewsfolder,'ID_{}.xml'.format(cID))
        rss_category[curtitle]['filepath'] = outputhtmlfilename
        wgg.GET(urlitem,outputhtmlfilename)
        cID += 1
    with open(os.path.join(rssnewsfolder,'rss_category.json'),'w') as fout:
        json.dump(rss_category,fout,indent = 4,sort_keys = True)


def get_current_time_str():
    datetimeobj = datetime.datetime
    date = datetimeobj.today()
    ret_str = ''
    ret_str += date.strftime('%Y_%m_%d')
    time = datetimeobj.now().time()
    ret_str += '_'
    ret_str += time.strftime('%H_%M_%S')
    return ret_str
def save_newsmat_to_json(newsmat,sinafolder):
    news_info = list()
    for item in newsmat:
        title = item[0].text
        url = item[1].text
        description = item[2].text
        phpindex = url.find(u'php?url=')
        url = url[phpindex+8:]
        title = title.strip(u'\r\n\t')
        # url = url.encode('utf-8')
        description = description.strip(u'\r\n\t')
        cur_news_dict = dict(title=unicode(title),url=url,description=description)
        news_info.append(cur_news_dict)
    return news_info

def crawl_sinanews_content():
    # craw all sub news page in sina rss xmls
    sinafolder = os.path.join(curfolderpath,'sina_news')
    rsspsr = rssParser()
    newsmat = rsspsr.parse_sina(sinafolder)
    news_info = save_newsmat_to_json(newsmat,sinafolder)
    # format:
    # (title,link,description)
    # ==============

    print '-'*10
    print 'total news urls: ',len(news_info)
    print '-'*10
    # crawl all url
    cur_timestr = get_current_time_str()
    savefolder = os.path.join(sinafolder,cur_timestr)
    if os.path.exists(savefolder)== False:
        os.mkdir(savefolder)
    wgg = wgetCrawl()
    news_count = 1
    for news_dict in news_info:
        cur_filepath = os.path.join(savefolder,'news_{}'.format(news_count))
        url = news_dict[u'url']
        news_dict['filepath']= cur_filepath
        wgg.GET(url,cur_filepath)
        news_count+=1
    # dump to json file
    json_filename = os.path.join(savefolder,'news_url_info.json')
    with codecs.open(json_filename,'w','utf-8') as fout:
        json.dump(news_info,fout,indent = 4,sort_keys = True,ensure_ascii= False)

def start_craw_rss_categories():
    crawl_sina_rss()
    crawl_sinanews_content()


if __name__ == '__main__':
    start_craw_rss_categories()
