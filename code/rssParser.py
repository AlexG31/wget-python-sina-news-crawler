#encoding:utf-8
"""
follow all the url items in xml file
"""

import os
import glob
import sys
import re
import codecs
import pdb
from bs4 import BeautifulSoup
import pdb
import xml.etree.cElementTree as ET

curfilepath = os.path.realpath('__file__')
curfolderpath = os.path.dirname(curfilepath)

# append current folder to system path
sys.path.append(curfolderpath)


from wgetCrawl import wgetCrawl

class rssParser:
    def __init__(self):
        pass
    def sina_is_valid_item(self,item):
        TextMaxThres = 400
        if item is None or len(item)<8:
            return False
        if item[0].tag != u'title' and item[1].tag != u'link':
            return False
        maxlen = 0
        for info in item:
            if info is None:
                return False
            textlen = 0
            if info.text is not None:
                textlen = len(info.text)
            if maxlen<textlen:
                maxlen = textlen
        if maxlen>TextMaxThres:
            return False
        return True
    def parse_sina(self,sinafolder):
        xmlfiles = glob.glob(os.path.join(sinafolder,'*.xml'))
        # record new data
        newsmat = []
        for xmlname in xmlfiles:
            print 'processing : {}'.format(xmlname)
            try:
                xmltree = ET.parse(xmlname)
            except Exception as e:
                print 'Exception! Cannot read xml file:{}\n\n'.format(xmlname)
            root = xmltree.getroot()
            items = root.findall('.//item')
            for item in items:
                if self.sina_is_valid_item(item) is True:
                    # print 'title:{}'.format(item[0].text.encode('utf-8'))
                    # print 'description:{}'.format(item[7].text.encode('utf8'))
                    # print u'url:{}'.format(item[1].text)
                    # print '='*30
                    newsmat.append((item[0],item[1],item[7]))
                    # pdb.set_trace()

        return newsmat


if __name__ == '__main__':
    # craw all sub news page in sina rss xmls
    sinafolder = os.path.join(curfolderpath,'news_txt','xinlangnews')
    rsspsr = rssParser()
    newsmat = rsspsr.parse_sina(sinafolder)
    # get url list
    urllist = []
    for item in newsmat:
        url = item[1].text
        phpindex = url.find(u'php?url=')
        url = url[phpindex+8:]
        urllist.append(url)
    # crawl all url
    savefolder = os.path.join(curfolderpath,'news_txt','sina_subnews')
    wgg = wgetCrawl()
    wgg.GET_urllist(urllist,savefolder)

