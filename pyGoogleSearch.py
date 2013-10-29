#-*- coding:utf-8 -*-
# original web data collecting class using Google Search Engine
# Byunghun Hwang <elecun2@gmail.com>

import mechanize
import os
import time

class collector:
    def __init__(self):
        self._browser = mechanize.Browser(factory=mechanize.RobustFactory())
        self._browser.set_handle_equiv(True)
        self._browser.set_handle_redirect(True)
        self._browser.set_handle_referer(True)
        self._browser.set_handle_robots(False)
        self._browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self._browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1')]

    def goNext(self, response):
        temp_index = response.rfind('Next')
        if temp_index < 0:
            return False

        buf = response[:temp_index]
        start_index = buf.rfind('href="')
        buf = response[start_index+len('href="'):temp_index]
        nextpage = 'http://www.google.com'+buf[0:buf.find('\"')]
        nextpage = nextpage.replace('amp;','')
        self._browser.open(nextpage)
        response = self._browser.response().read()
        return response

    def search(self, workingPath, keyword, nmax):
        orgPath = workingPath + '\\' + keyword + '\\org\\'

        #create folder
        if os.path.exists(orgPath)==False:
            os.mkdir(orgPath)

        #검색
        self._browser.open('http://www.google.com/search?hl=en&q='+keyword+'&lr=lang_en')
        response = self._browser.response().read()

        #결과저장
        orgFile = file(orgPath + keyword + '.txt','w')
        orgFile.write(response)
        orgFile.close()

        #url list
        urllist = []
        urllist = self.getURLs(response, urllist, nmax)

        #max가 될때까지 url 추출.
        while len(urllist)<nmax:
            response = self.gotoNextSearch(orgPath, keyword, response)
            if response == '':
                break
            self.getURLs(response, urllist, nmax)

        return urllist

    def gotoNextSearch(self, directory, keyword, response):
        temp_index = response.rfind('Next')
        if temp_index < 0:
            return ''

        #next page 주소 추출
        buf = response[:temp_index]
        start_index = buf.rfind('href="')
        buf = response[start_index+len('href="'):temp_index]
        nextPage = 'http://www.google.com' + buf[0:buf.find('"')]
        nextPage = nextPage.replace('amp;','')

        #go to next page
        self._browser.open(nextPage)
        response = self._browser.response().read()
        
        return response

    #검색결과에서 result URL을 추출한다. <h3 class="r"> tag뒤에 나오는 url을 가져온다.
    def getURLs(self, response, urllist, nmax):
        start_index = 0
        while  start_index > -1:
            start_index = response.find('<h3 class="r">', start_index)

            if start_index <0:
                start_index = 0
                break
            
            start_index = response.find('<a href="',start_index)+len('<a href="')
            end_index = response.find('"',start_index+1)
            url = str(response[start_index:end_index])

            urllist.append(url)
            nURL = len(urllist)
            print '[%3.1f%%(%d/%d)] : '%((float(nURL)/float(nmax)*100.0),nURL,nmax)+url
            if nURL==nmax:
                break

        return urllist