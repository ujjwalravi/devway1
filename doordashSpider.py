# -*- coding: utf-8 -*-
import scrapy
import os
from selenium import webdriver
from pydispatch import dispatcher
from scrapy import signals
import json

from doordash.items import DoordashItem
from webdriver_manager.chrome import ChromeDriverManager
import traceback
from scrapy.http import Request
import time
class DoordashspiderSpider(scrapy.Spider):

    name = 'doordashSpider'
    allowed_domains = ['doordash.com']

    counter = 0
    results = {}

    #def __init__(self):
        #dispatcher.connect(self.spider_closed, signals.spider_closed)


    def __init__(self, *args, **kwargs):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/80.0.3987.132 Safari/537.36'
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--disable-dev-shm-usage')
        chrome_option.add_argument('--ignore-certificate-errors')
        chrome_option.add_argument("--disable-blink-features=AutomationControlled")
        chrome_option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36')
        #chrome_option.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        self.driver = webdriver.Chrome( options = chrome_option)
        self.url = 'https://www.doordash.com/'

    def start_requests(self):
        count = 1
        num = 1

        try:
            lst = []

            self.driver.get(self.url)
            time.sleep(18)

            input_ = self.driver.find_element_by_xpath("//input[@aria-label='Your delivery address']")
            input_.send_keys("portland")
            time.sleep(15)
            self.driver.find_element_by_xpath("//button[@aria-label='Find Restaurants']").click()
            time.sleep(15)
            NAME = 'NAME'
            DESCRIPTION ='DESCRIPTION'
            PRICE = 'PRICE'
            while 1>0:
                if count == 1:
                    resturl = self.driver.find_elements_by_class_name('sc-hAcydR')
                    for i in resturl:
                        lst.append(i.get_attribute('href'))
                    print(lst)

                    time.sleep(1)
                    for n in lst:
                        time.sleep(5)
                        print(n)
                        Menu = {}
                        #fullurl = "https://www.doordash.com" + n
                        #print(fullurl)
                        self.driver.execute_script("window.open('');")
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        self.driver.get(n)
                        time.sleep(15)
                        #Inside New Tab
                        print("SUCCESS")
                        restname = self.driver.find_element_by_class_name("sc-dDJTWM").text
                        print(restname)   #Restaurant name
                        RestName = restname
                        timing = self.driver.find_element_by_class_name("hlXfBB").text
                        print(timing)   #Timings
                        Timee = timing
                        ratings = self.driver.find_element_by_class_name("xdlgy").text
                        print(ratings)  #ratings
                        Ratings = ratings
                        deliveryfee = self.driver.find_element_by_class_name("eFwXTH").text
                        print(deliveryfee)  #deliveryfee
                        DelFee = deliveryfee
                        menuname = self.driver.find_elements_by_class_name("gImhEG")

                        for a in menuname:
                            print(a.text)
                            Menu[NAME] = a.text
                        menudescript = self.driver.find_elements_by_class_name("huydyu")
                        for b in menudescript:
                            print(b.text)
                            Menu[DESCRIPTION] = b.text
                        menuprice = self.driver.find_elements_by_class_name("hpbvJT")
                        for c in menuprice:
                            print(c.text)
                            Menu[PRICE] = c.text
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

                        num=num+1
                        print(num)


                        #time.sleep(1)
                        self.results[self.counter] = {
                            "Resname": RestName,
                            "Timee": Timee,
                            "Ratings": Ratings,
                            "Menu": Menu

                            }
                        self.counter = self.counter + 1
                        if num == 2:
                            break


                    yield Request("http://testscript.com/", callback=self.parse, meta={'name_lst':lst})
                    print(lst)
                    print("COMPLETED SUCCESS")

                if num == 2:
                    break
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print('No of pages Scrolled (out of  24)', count)
                time.sleep(15)  #according to my Internet Speed
                count = count + 1
            #self.parse(lst)
        except:
            print(traceback.print_exc())
            print("element not found..")

    def parse(self, response):
        item = DoordashItem()
        item['restaurant_name'] = response.meta.get('name_lst')
        yield item


    def spider_closed(self, spider):
        with  open('results.json', 'w') as fp:
            json.dump(self.results, fp)
