import sys

sys.path.append('../')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import json
from lxml import etree
from settings import COOKIES_PATH, PIC_SWITCH, PAGE, START_URL
import re


class BrowserCrawl:
    def __init__(self):
        self.url = START_URL
        self.opitions = self.newOptions()
        self.browser = self.newBrowser()
        # self.wait = WebDriverWait(self.browser, 10)

    def newOptions(self):
        options = webdriver.ChromeOptions()
        header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/{} (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/{}'
        num = str(float(random.randint(500, 600)))
        # 添加header
        options.add_argument("user-agent=" + header.format(num, num))
        # 禁止加载图片
        if PIC_SWITCH:
            dlp = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
            options.add_experimental_option('prefs', dlp)
        return options

    def newBrowser(self):
        browser = webdriver.Chrome(options=self.opitions)
        # 消除browser的驱动标签
        browser.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => False,});')
        return browser

    # 添加cookies
    def addCookies(self):
        self.browser.get(self.url)
        with open('../../taobao_cookie', 'r', encoding='utf-8') as f:
            cs = json.load(f)
        for c in cs:
            self.browser.add_cookie(c)

    def search(self):
        searchText = self.browser.find_element_by_xpath('//input[@aria-haspopup="true"]')
        product = input("what do you want to search:\n")
        searchText.send_keys(product)
        searchText.send_keys(Keys.ENTER)
        time.sleep(random.randint(2, 4))
        ref = self.browser.find_element_by_xpath('//input[contains(@class,"input J_Input")]')
        ref.clear()
        ref.send_keys('2')
        wait = WebDriverWait(self.browser, 10)
        ref.send_keys(Keys.ENTER)
        try:
            wait.until(
                EC.text_to_be_present_in_element_value((By.XPATH, '//input[contains(@class,"input J_Input")]'), '3'),
                "reload error!")
            time.sleep(random.randint(2, 3))
        except Exception as e:
            self.browser.close()

    def getPage(self, url):
        print("crawling: ", url)
        try:
            self.browser.get(url)
            return self.browser.page_source
        except Exception as e:
            print(e)

    # xpath解析页面
    def parsePage(self, page):
        html = etree.HTML(page)
        items = html.xpath('//div[contains(@class,"price g_price g_price-highlight")]/strong/text()')
        return items

    # 保存页面
    def savePage(self, page):
        for item in page:
            print(item)

    # 单个页面的爬取调度
    def schedule(self, url):
        page = self.getPage(url)
        html = self.parsePage(page)
        self.savePage(html)

    def run(self):
        try:
            self.addCookies()
            self.search()
            url = re.sub('(s=\d+)|(data-value=\d+)', '', self.browser.current_url, 2) + 's={offset}'
            for p in range(1, PAGE):
                self.schedule(url.format(offset=(p - 1) * 44))
                time.sleep(random.randint(2, 4))
            print("crawl done!")
        except Exception as e:
            print(e)
        finally:
            self.close()

    def close(self):
        self.browser.close()

if __name__ == '__main__':
    t = BrowserCrawl()
    t.run()
