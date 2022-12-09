import scrapy
import time
import datetime
import requests
import json
import pandas as pd
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
from newscrawling.items import NewscrawlingItem

 
class NewsUrlSpider(scrapy.Spider):
    name = "newsUrlCrawler"
 
    def start_requests(self):
        Maincats = ['politics', 'economic']
        for Maincat in Maincats:
            if Maincat == 'politics':
                subcategorys = ['assembly','north','others','dipdefen','president']
            else:
                subcategorys = ['finance',' industry',' employ','others','autos','stock','stock/market','stock/publicnotice','stock/world','stock/bondsfutures','stock/fx','stock/others','estate','consumer','world']
            #정치(politics) = ['assembly', 'north', 'others', 'dipdefen',' president']
            #경제(economic) = ['finance',' industry',' employ','others','autos','stock','stock/market','stock/publicnotice','stock/world','stock/bondsfutures','stock/fx','stock/others','estate','consumer','world']

            start = datetime.strptime('20221029', "%Y%m%d")
            end = datetime.strptime('20221129', '%Y%m%d')
            dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]
            for subcategory in subcategorys:
                for date in dates:
                    print(date)
                    for pagenum in range(1,50):
                        BASE_URL = 'https://news.daum.net/breakingnews/{main}/{subcat}?page={num}&regDate={date}'.format(main=Maincat,subcat=subcategory ,num=pagenum, date=date)
                        res = requests.get(BASE_URL)
                        soup = BeautifulSoup(res.text, 'html.parser')
                        
                        try:
                            soup.find('em', class_="num_page").text.split(str(pagenum))[1]
                            urls = soup.find_all('a', class_='link_thumb')
                            
                            for url in urls:
                                print(url['href'])
                                yield scrapy.Request(url=url['href'],callback=self.parse_news, headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}, meta={'Maincat':Maincat, 'subcategory':subcategory})
                        except:
                            print('다음 date로')
                            break



    def parse_news(self, response):
        item = NewscrawlingItem()
        
        item['MainCategory'] = response.meta['Maincat']
        item['SubCategory'] = response.meta['subcategory']
        item['WritedAt'] = response.xpath('//*[@id="mArticle"]/div[1]/div[1]/span[2]/span/text()').extract()
        item['Title'] = response.xpath('//*[@id="mArticle"]/div[1]/h3/text()').extract()
        item['Content'] = response.xpath('//*[@id="mArticle"]/div[2]/div[2]/section/div[contains(@dmcf-ptype, "general")]/text()').extract()+response.xpath('//*[@id="mArticle"]/div[2]/div[2]/section/p[contains(@dmcf-ptype, "general")]/text()').extract()
        item['URL'] = response.url
        item['Writer'] = response.xpath('//*[@id="mArticle"]/div[1]/div[1]/span[1]/text()').extract()
        item['Press'] = response.xpath('//*[@id="kakaoServiceLogo"]/text()').extract()
        news_id=response.url.split('v/')[-1]
        url = 'https://action.daum.net/apis/v1/reactions/home?itemKey={}'.format(news_id)
        header = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "referer": url,
            'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb3J1bV9rZXkiOiJuZXdzIiwidXNlcl92aWV3Ijp7ImlkIjoyMDgwMzkwNiwiaWNvbiI6Imh0dHBzOi8vdDEuZGF1bWNkbi5uZXQvcHJvZmlsZS9JZWt0Z3lzOGkyMTAiLCJwcm92aWRlcklkIjoiREFVTSIsImRpc3BsYXlOYW1lIjoi7Jik7Zqo7KSAIn0sImdyYW50X3R5cGUiOiJhbGV4X2NyZWRlbnRpYWxzIiwic2NvcGUiOltdLCJleHAiOjE2Njk4NDg4ODQsImF1dGhvcml0aWVzIjpbIlJPTEVfREFVTSIsIlJPTEVfSURFTlRJRklFRCIsIlJPTEVfVVNFUiJdLCJqdGkiOiJlYzA4NjJmOC1jZWY2LTRmMTMtYTkwNy05MDk2ODNiYWVmNjIiLCJmb3J1bV9pZCI6LTk5LCJjbGllbnRfaWQiOiIyNkJYQXZLbnk1V0Y1WjA5bHI1azc3WTgifQ.XCwfHH2woBK2A9d5udVlzqlvkIeFQEiT7-9rvd538l8'}
        raw = requests.get(url, headers=header)
    
        s_jsonData = json.loads(raw.text)
        s_jsonData
    
        sentiment = {"좋아요" : 0, "감동이에요" : 0, "슬퍼요" : 0, "화나요" : 0, "추천해요" : 0}
    
        sentiment['좋아요'] = s_jsonData['item']['stats']['LIKE']
        sentiment['감동이에요'] = s_jsonData['item']['stats']['IMPRESS']
        sentiment['슬퍼요'] = s_jsonData['item']['stats']['SAD']
        sentiment['화나요'] = s_jsonData['item']['stats']['ANGRY']
        sentiment['추천해요'] = s_jsonData['item']['stats']['RECOMMEND']
        item['Stickers'] = sentiment
        
        print('*'*100)
        print(item['MainCategory'])
        print(item['SubCategory'])
        print(item['Title'])
        print(item['URL'])
        print(item['WritedAt'])
        print(item['Stickers'])
        
        return item


class NewsSpider(scrapy.Spider):
    name = "newsCrawler"
 
    def start_requests(self):
        data = pd.read_csv('/Users/joon/workspace/newscrawling/all_crawling.csv')
        for i in data['URL']:
            yield scrapy.Request(url=i, callback=self.parse_news, headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
 
    def parse_news(self, response):
        item = NewscrawlingItem()

        list_comment = []
        url = 'https://comment.daum.net/apis/v1/posts/@{}/comments?'.format(response.url.split('v/')[-1])
        params = {'parentId' : '0', 'offset' : '0', 'limit' : '100', 'sort' : 'RECOMMEND', 'isInitial' : 'true'}
        headers = {'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb3J1bV9rZXkiOiJuZXdzIiwidXNlcl92aWV3Ijp7ImlkIjoyMDgwMzkwNiwiaWNvbiI6Imh0dHBzOi8vdDEuZGF1bWNkbi5uZXQvcHJvZmlsZS9JZWt0Z3lzOGkyMTAiLCJwcm92aWRlcklkIjoiREFVTSIsImRpc3BsYXlOYW1lIjoi7Jik7Zqo7KSAIn0sImdyYW50X3R5cGUiOiJhbGV4X2NyZWRlbnRpYWxzIiwic2NvcGUiOltdLCJleHAiOjE2Njk4OTUxNjEsImF1dGhvcml0aWVzIjpbIlJPTEVfREFVTSIsIlJPTEVfSURFTlRJRklFRCIsIlJPTEVfVVNFUiJdLCJqdGkiOiI2YjUwMGJmNS0zYzZkLTRiOWMtOTVmNS03NzQxM2MzODUyOGIiLCJmb3J1bV9pZCI6LTk5LCJjbGllbnRfaWQiOiIyNkJYQXZLbnk1V0Y1WjA5bHI1azc3WTgifQ.Fx1U6aXn0-hYz3wPjVQ6TAAFSL7nDLLyq1kbMkFeVp0'}
        response = requests.get(url, headers = headers, params = params)
        status_code = response.status_code
        comment_all = response.json()
        # print(response.json())
        # print(count_all['commentCount'])
        for i in comment_all:
            item['URL'] = 'https://v.daum.net/v/'+response.url.split('/')[-2].split('@')[-1]
            item['NewsID'] = response.url.split('/')[-2].split('@')[-1]
            item['Content'] = i['content']
            item['UserID'] = i['userId']
            item['UserName'] = i['user']['displayName']
            item['WritedAt'] = i['createdAt']
            
            #print(li)
            #print("----")
        
        if len(list_comment) == 0:
            list_comment.append('NA')



        print(item['URL'])
        print(item['UserName'])
        print(item['NewsID'])
        print(item['WritedAt'])

 
        yield item


