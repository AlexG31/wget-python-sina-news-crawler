#!/usr/local/bin/python
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
import glob
from bs4 import BeautifulSoup
import pdb

# gpf newsParser
from newsParser import newsParser
from HtmlContentRenderer import HtmlContentRenderer
from newsContentParser import  newsContentParser
curfilepath = os.path.realpath('__file__')
curfolderpath = os.path.dirname(curfilepath)
#debug
print 'curfolder path:',curfolderpath

# append current folder to system path
sys.path.append(curfolderpath)


def refreshhtml(newsmat):
    rnder = HtmlContentRenderer()
    rnder.load_labnews(os.path.join(curfolderpath,'htmltemplates'),newsmat)

def parseFolder(savefolderpath = None):
    # save csv to folder
    if savefolderpath is None:
        savefolderpath = os.path.join(curfolderpath,'news_data')
    subhtmllist = glob.glob(os.path.join(curfolderpath,'news_txt','sina_subnews','*.html'))
    targetfile = subhtmllist[3]
    # csv mat data
    newscontentMat = []
    for targetfile in subhtmllist:
        print 'target file:',targetfile
        try:
            with codecs.open(targetfile,'r','utf-8') as fin:
                psr = newsContentParser(fin)
                title,content = psr.parse()

                #for csv
                curfilename = os.path.split(targetfile)[-1]
                if '.' in curfilename:
                    curfilename = curfilename[0:curfilename.find('.')]
                # process content to <p> </p> string
                contentstr = u'<p>'+u'</p>\n<p>'.join(content)+u'</p>'
                newscontentMat.append({'newstitle':title,'newstitleID':curfilename,'newscontent':contentstr})
                # print 'title:',title
                # print 'content:',content
                # pdb.set_trace()
        except UnicodeDecodeError:
            print 'file:{}'.format(targetfile)
            print 'utf8 decode error!'
            pass
    return newscontentMat


if __name__== '__main__':
    newsmat = parseFolder()
    refreshhtml(newsmat)
    pass


