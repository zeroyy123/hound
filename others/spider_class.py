# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

class spider():
    def __init__(self):
        self.driver = []
        self.results = pd.DataFrame({})

    def open_web_driver(self,proxy_ip='',webdrv=''):
        PROXY = proxy_ip # IP:PORT or HOST:PORT
        if proxy_ip == 'null':
            proxy_ip = ''
        if webdrv == 'PhantomJS':
            service_args = [
                                '--proxy='+proxy_ip ,
                                '--proxy-type=http',
                                '--load-images=no',
                                # '--disk-cache=yes',
                            ]
            self.driver = webdriver.PhantomJS(service_args=service_args)
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("user-data-dir="+ os.path.abspath(r"C:\Users\yy\AppData\Local\Google\Chrome\User Data"))
            if PROXY != '':
                chrome_options.add_argument('--proxy-server=http://'+PROXY)
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def open_web_url(self,url): ## need subclass to edit
        pass

    def open_web(self,proxy_ip='',webdrv='',url=''):
        self.open_web_driver(proxy_ip,webdrv)
        self.open_web_url(url)

    def search_item(self,target): ## need subclass to edit
        pass

    def get_index(self): ## need subclass to edit
        pass

    def get_search_count(self): ## need subclass to edit
        pass
        
    def get_page_num(self): ## need subclass to edit
        pass

    def get_item(self):  ## need subclass to edit
        pass

    def go_page(self,page): ## need subclass to edit
        pass
        
    def next_page(self):
        pass

    def driver_quit(self):
        self.driver.quit()

    def open_mode_sel(self,target,proxy_ip='',webdrv='',url=''):
        if url == '':
            self.open_web(proxy_ip,webdrv)
            self.search_item(target)  ## use search as entrance
            js="var q=document.body.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(0.5)
        else:
            self.open_web(proxy_ip,webdrv,url)
            js="var q=document.body.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(0.5)

    def save_xlsx(self,target):
        writer = pd.ExcelWriter('data/' + target+'.xlsx', engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        self.results.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def process_get_index(self,proxy_ip='',webdrv=''):
        self.open_mode_sel(target='',proxy_ip=proxy_ip,webdrv=webdrv,url='')
        self.get_index()
        self.driver_quit()

    def process(self,target,proxy_ip='',webdrv='',page_max=1000,url=''):  # if url == '', process will search target in the web as entrance
        self.open_mode_sel(target,proxy_ip,webdrv,url)

        search_count = self.get_search_count()
        print 'search_count:',search_count
        
        page_num = self.get_page_num()
        print 'page_max:',page_num
        
        if page_max > page_num:
            page_max = page_num
        print page_max
        
        for i in range(page_max):
            print target,': ',i
            state = self.get_item()
            if state == 'no items':
                break
            elif state == 'error':
                break

            if i%10 == 9:
                print 'web driver restart'
                curr_url = self.driver.current_url
                print curr_url
                self.driver_quit()
                self.open_mode_sel(target,proxy_ip,webdrv,curr_url)

            if len(self.results) >= search_count:
                break
            if i < (page_max - 1):
                try:
                    self.next_page()
                except:
                    print 'click next page fail'
                    break
##                self.go_page(i+2)  ## phantomjs cann't use send key
        
        self.driver_quit()
        self.results.to_csv('data/'+target+'.csv',encoding='utf-8')
        self.save_xlsx(target)

##        print self.results
        print 'results number :',len(self.results)
        print 'finish'











