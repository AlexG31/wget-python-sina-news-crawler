#encoding:utf-8
"""
follow all the linked text in the home page of news sites
1. do some filtering with the links
2. check for repeat links
"""

import os
import glob
import sys
import re
import codecs
import pdb
from bs4 import BeautifulSoup
import pdb

# gpf newsParser
from newsParser import newsParser

curfilepath = os.path.realpath('__file__')
curfolderpath = os.path.dirname(curfilepath)
#debug
#print 'curfolder path:',curfolderpath


# append current folder to system path
sys.path.append(curfolderpath)


class wgetCrawl:
    def __init__(self):
        pass
    def GET(self,url,outputfilename):
        cmdstr = u'wget {} -O {}'.format(url,outputfilename)
        print u'command:[{}]'.format(cmdstr)
        cmdstr = cmdstr.encode('utf-8')
        #pdb.set_trace()
        os.system(cmdstr)
    def GET_urllist(self,urllist,savefolderpath):
        # output
        cID = 1
        for url in urllist:
            url = unicode(url)
            outputhtmlfilename = unicode(os.path.join(savefolderpath,'ID_{}.html'.format(cID)))
            self.GET(url,outputhtmlfilename)
            cID += 1

    def page_crawl(self,homepagefilename,outputfolder):
        with codecs.open(homepagefilename,'r','gbk') as fin:
            print 'crawing file:{}'.format(homepagefilename)
            parser = newsParser(fin)
            urldict = parser.parse_subnews_url()
            # output
            cID = 1
            for url in urldict.iterkeys():
                # debug
                if cID<127:
                    cID+=1
                    continue
                url = unicode(url)
                outputhtmlfilename = unicode(os.path.join(outputfolder,'ID_{}.html'.format(cID)))
                self.GET(url,outputhtmlfilename)
                cID += 1
    def crawl_sina_rss(self):
        xmlfilepath = os.path.join(curfolderpath,'news_txt','sina_all_opml.xml')
        with codecs.open(xmlfilepath,'r','utf8') as fin:
            psr = newsParser(fin)
            title,contenturl = psr.parse_sina_xml()
        rssnewsfolder = os.path.join(curfolderpath,'news_txt','xinlangnews')
        # craw each content url
        cID = 1
        for urlitem in contenturl:
            outputhtmlfilename = os.path.join(rssnewsfolder,'ID_{}.xml'.format(cID))
            self.GET(urlitem,outputhtmlfilename)
            cID += 1




if __name__ == '__main__':
    wgg = wgetCrawl()
    wgg.crawl_sina_rss()
    # wgg.page_crawl(os.path.join(curfolderpath,'news_txt','newsbaidu.txt'),os.path.join(curfolderpath,'news_txt','baidunews'))
    
