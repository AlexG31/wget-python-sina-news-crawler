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

curfilepath = os.path.realpath('__file__')
curfolderpath = os.path.dirname(curfilepath)

# append current folder to system path
sys.path.append(curfolderpath)


class newsParser:
    # file pointer for html file
    targeturl = 'news.baidu.com'
    fp = None
    newslinks = None
    newstitles = None
    links2titlesdict = None
    # ======================
    # url: title(longest)
    # ======================
    urldict = dict()
    
    def __init__(self,fin):
        if not fin:
            raise StandardError('File handle failed!')
        self.fp = fin
    
    def get_title_content_from_html(self):
        # patter search for news title and url
        pat = re.compile(r'<[^>]*a href="(http[^"]+)[^>]* target="_blank"[^>]*>([^<]*)<\/a>',re.UNICODE)
        newstitles = list()
        # repeat links
        linksdict = dict()

        for line in self.fp:
            res = pat.findall(line)
            if len(res) ==0:
                continue
            for ltpair in res:
                if ltpair[0] not in linksdict:
                    linksdict[ltpair[0]] = ltpair[1]
                    newstitles.append(ltpair[1])
        self.links2titlesdict = linksdict
        self.newslinks = linksdict.keys()
        self.newstitles = newstitles

    def newstitles(self):
        if self.newstitles:
            return self.newstitles
        # parse html text first
        self.get_title_content_from_html()
        return self.newslinks

    def newslinks(self):
        if self.newslinks:
            return self.newslinks
        # parse html text first
        self.get_title_content_from_html()
        return self.newslinks
    def links_to_titles_dict(self):
        if len(self.urldict) > 0:
            return self.urldict
        # parse html text first
        return self.parse_subnews_url()
    def parse_sina_xml(self):
        #with codecs.open(filepath,'r','utf-8') as fin:
        # find all <p> with length > para_min_len
        # 1. without any attributes
        # 2. length
        # 
        MIN_CONTENT_LEN = 20
        soup = BeautifulSoup(self.fp,'lxml')

        title , contenturl = [],[]

        print '--- Title ---'
        if soup.title is None:
            print 'Title is [None]'
            return
        print '[title]:',soup.title
        print '-'*10
        ptlist = soup.find_all('outline')
        for line in ptlist:
            if not line:
                continue
            attrs = line.attrs
            # target url not in line
            if 'xmlurl' not in attrs:
                continue
            print 'Attributes:',line.attrs
            print 'xmlURL:[{}]'.format(attrs['xmlurl'])
            title.append(attrs['title'])
            contenturl.append(attrs['xmlurl'])
        return (title,contenturl)

    def parse_subnews_content(self):
        #with codecs.open(filepath,'r','utf-8') as fin:
        # find all <p> with length > para_min_len
        # 1. without any attributes
        # 2. length
        # 
        MIN_CONTENT_LEN = 20
        soup = BeautifulSoup(self.fp,'lxml')

        title = soup.title.string if soup.title is not None else '[None]'
        contentlist = []

        ptlist = soup.find_all('p')
        for line in ptlist:
            if not line:
                continue
            attrs = line.attrs
            #print 'Attributes:',line.attrs
            if len(attrs) == 0:
                #print 'Contents:',line.contents
                if line.string:
                    contentlist.append(line.string)
                else:
                    for cont in line.contents:
                        if cont.name is None:
                            contentlist.append(cont.string)
                        elif cont.name == 'a':
                            contentlist.append('[url] {}'.format(cont.string))
        content = '\n'.join(contentlist)
        return (title,content)
    def parse_subnews_url(self):
        #with codecs.open(filepath,'r','utf-8') as fin:
        # find all <p> with length > para_min_len
        # 1. without any attributes
        # 2. length

        soup = BeautifulSoup(self.fp,'lxml')
        if soup.title is None:
            return
        ptlist = soup.find_all('a')
        for link in ptlist:
            # filter out those none-news url
            if link is None or link.string is None:
                continue
            if len(link.string) <=5:
                continue
            # print 'news link title:'
            # print link.string
            # print 'news url :'
            # print link['href']
            # print 'news url to filename :'
            # print phloader.url2filename(link['href'])
            # add to urldict
            link_url = link['href']
            if link_url in self.urldict:
                if len(link.string) > len(self.urldict[link_url]):
                    self.urldict[link_url] = link.string
            else:
                self.urldict[link_url] = link.string
        return self.urldict
            
            
            
def parse_single_homepage():
    resfolder = os.path.join(curfolderpath,'news_txt')
    resfiles = glob.glob(os.path.join(resfolder,'*.txt'))
    targetfilepath = resfiles[0]
    with codecs.open(targetfilepath,'r','GBK') as fin:
        print 'processing filename: {}'.format(targetfilepath)
        parser = newsParser(fin)
        parser.parse_subnews_url()
        # write to csv file
        csvmat = []
        with codecs.open(os.path.join(curfolderpath,'tmp.out'),'w','utf-8') as fout:
            for url,utitle in parser.urldict.iteritems():
                url = unicode(url)
                utitle = unicode(utitle)
                csvmat.append((url,utitle))
                fout.write(u'[url:{}]->({})\n'.format(url,utitle))
        # write to csv file
        from csvwriter import CSVwriter
        csv = CSVwriter(os.path.join(curfolderpath,'homepageurl.csv'))
        csv.output(csvmat)



def try_parse_sina_xml():
    xmlfilepath = os.path.join(curfolderpath,'news_txt','sina_all_opml.xml')
    with codecs.open(xmlfilepath,'r','utf8') as fin:
        psr = newsParser(fin)
        psr.parse_sina_xml()
if __name__ == "__main__":
    # parse_single_homepage()
    try_parse_sina_xml()
