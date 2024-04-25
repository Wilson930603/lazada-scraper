import json, scrapy,re,json,html,os,platform
from datetime import datetime,timedelta
from crawldata.functions import *
class CrawlerSpider(scrapy.Spider):
    name = 'product_detail'
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+datetime.now().strftime("%Y-%m-%d_%H.%M.%S")+'.log'}
    cookies = {'userLanguageML': 'en'}
    headers_json = {'Accept': 'application/json','Accept-Language': 'en-GB,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Content-Type': 'application/json','Authorization': 'Bearer','sourceCode': '','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','TE': 'trailers',}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-GB,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1','Cache-Control': 'max-age=0',}
    DATE_CRAWL=(datetime.now()+timedelta(1)).strftime('%Y-%m-%d')
    REIVEWS=['reviewRateId','buyerId','buyerName','reviewTitle','rating','reviewContent','reviewTime','likeCount','helpful','rejected','reviewTime','images','replies','isPurchased']
    domain='https://www.lazada.co.th'
    lang='en'
    reviews=0
    if platform.system()=='Linux':
        URL='file:////' + os.getcwd()
    else:
        URL='file:///' + os.getcwd()
    SEARCH_LIST=[]
    LIMIT=10
    def __init__(self, lang=None, reviews=None, **kwargs):
        if lang:
            self.lang=str(lang).strip()
            self.cookies['userLanguageML']=lang
        if reviews:
            self.reviews=int(reviews)
        super().__init__(**kwargs)
    def start_requests(self):
        files=os.scandir('./Data/')
        FILES=[]
        for f in files:
            if str(f.name).startswith('search_result_'):
                FILES.append(f.name)
        for i in range(len(FILES)):
            print(i,' -',FILES[i])
        SELECT=input('Input the number of file will get detail:')
        print('Start crawl product detail from: ', FILES[int(SELECT)])
        url=self.URL+'/Data/'+FILES[int(SELECT)]
        yield scrapy.Request(url,callback=self.parse_list_url,meta={'proxy':None})
    def parse_list_url(self,response):
        Data=json.loads(response.text)
        for ROW in Data:
            self.SEARCH_LIST.append(ROW)
        for No in range(self.LIMIT):
            if No<len(self.SEARCH_LIST):
                ROW=self.SEARCH_LIST[No]
                yield scrapy.Request(ROW['url'],callback=self.parse_details,meta={'ROW':ROW,'Level':0,'No':No},dont_filter=True,headers=self.headers,cookies=self.cookies)
    def parse_details(self,response):
        ROW=response.meta['ROW']
        Level=response.meta['Level']
        No=response.meta['No']
        if not ('"action":"captcha"' in str(response.text).replace(' ','')) and not('FAIL_SYS_USER_VALIDATE' in response.text):
            if '__moduleData__ = {' in response.text:
                HTML='{'+str(response.text).split('__moduleData__ = {')[1].split('};')[0]+'}'
                Data=json.loads(HTML)
                Data1=json.loads(response.xpath('//script[@type="application/ld+json"]/text()').get())
                ITEM={}
                ITEM['Data']=Data
                ITEM['Data1']=Data1
                IT={}
                IT=get_item_from_json(IT,ITEM,'')
                IMG=[]
                i=0
                while i<=20:
                    if 'Data.data.root.fields.skuGalleries.0.'+str(i)+'.type' in IT:
                        if IT['Data.data.root.fields.skuGalleries.0.'+str(i)+'.type']=='img':
                            IMG.append('https:'+IT['Data.data.root.fields.skuGalleries.0.'+str(i)+'.src'])
                    i+=1
                DES=response.xpath('//div[@class="module-detailImageText"]//p').get()
                HTML=''
                if 'Data.data.root.fields.product.highlights' in IT:
                    HTML+=IT['Data.data.root.fields.product.highlights']
                if 'Data.data.root.fields.product.desc' in IT:
                    HTML+=IT['Data.data.root.fields.product.desc']
                if DES:
                    HTML+=DES
                ROW['description']=HTML
                ROW['categories']=Data['data']['root']['fields']['tracking']['pdt_category']
                ROW['thumbs']=IMG
                MD=[]
                try:
                    for rs in Data['data']['root']['fields']['productOption']['skuBase']['properties'][0]['values']:
                        MD.append(rs['name'])
                except:
                    pass
                ROW['models']=MD
                ROW['recommendation_products']=[]
                ROW['reviews']=[]
                url='https://pdpdesc-m.lazada.co.th/recommend?'+Data['data']['root']['fields']['globalConfig']['recommendParameter']
                yield scrapy.Request(url,callback=self.parse_recommend,meta={'ROW':ROW,'Level':0,'No':No},headers=self.headers_json,cookies=self.cookies)
        else:
            if Level<10:
                Level+=1
                yield scrapy.Request(row['url'],callback=self.parse_shop,meta={'ROW':row,'Level':Level,'No':No},dont_filter=True,cookies=self.cookies,headers=self.headers)
            else:
                print('\n-----------')
                print('OUT: parse_details')
    def parse_recommend(self,response):
        ROW=response.meta['ROW']
        Level=response.meta['Level']
        No=response.meta['No']
        if not ('"action":"captcha"' in str(response.text).replace(' ','')) and not('FAIL_SYS_USER_VALIDATE' in response.text):
            try:
                DATA=json.loads(response.text)
                for k,row in DATA['data'].items():
                    if 'recommendType' in row and row['recommendType']=="v2v":
                        for i in range(10):
                            if i<len(row['products']):
                                rs=row['products'][i]
                                item={}
                                item['title']=rs['title']
                                item['url']='https:'+rs['link']
                                item['price']=rs['salePrice']
                                item['iamge']='https:'+rs['image']
                                item['sold_count']=rs['soldCnt']
                                item['rating_score']=rs['ratingNumber']
                                ROW['recommendation_products'].append(item)
                url='https://my.lazada.co.th/pdp/review/getReviewList?itemId='+ROW['itemId']+'&pageSize=50&filter=0&sort=0&pageNo=1'
                yield scrapy.Request(url,callback=self.parse_reviews,meta={'ROW':ROW,'Level':0,'reviews':0,'No':No},headers=self.headers_json,cookies=self.cookies)
            except:
                if Level<10:
                    Level+=1
                    yield scrapy.Request(response.url,callback=self.parse_recommend,headers=self.headers_json,meta={'ROW':ROW,'Level':Level,'No':No},dont_filter=True)                    
        else:
            if Level<10:
                Level+=1
                yield scrapy.Request(response.url,callback=self.parse_recommend,headers=self.headers_json,meta={'ROW':ROW,'Level':Level,'No':No},dont_filter=True)
            else:
                print('\n-----------')
                print('OUT: parse_recommend')
    def parse_reviews(self,response):
        ROW=response.meta['ROW']
        Level=response.meta['Level']
        reviews=response.meta['reviews']
        No=response.meta['No']
        if not ('"action":"captcha"' in str(response.text).replace(' ','')) and not('FAIL_SYS_USER_VALIDATE' in response.text):
            try:
                DATA=json.loads(response.text)
                for row in DATA['model']['items']:
                    if self.reviews==0 or reviews<self.reviews:
                        item={}
                        for k in self.REIVEWS:
                            if k in row:
                                item[k]=row[k]
                            else:
                                item[k]=''
                        ROW['reviews'].append(item)
                        reviews+=1
                if DATA['model']['paging']['currentPage']<DATA['model']['paging']['totalPages'] and (self.reviews==0 or reviews<self.reviews):
                    url='https://my.lazada.co.th/pdp/review/getReviewList?itemId='+ROW['itemId']+'&pageSize=50&filter=0&sort=0&pageNo='+str(DATA['model']['paging']['currentPage']+1)
                    yield scrapy.Request(url,callback=self.parse_reviews,meta={'ROW':ROW,'Level':0,'reviews':reviews,'No':No},headers=self.headers_json,cookies=self.cookies)
                else:
                    yield(ROW)
                    No_Next=No+self.LIMIT
                    if No_Next<len(self.SEARCH_LIST):
                        ROW_NEXT=self.SEARCH_LIST[No_Next]
                    yield scrapy.Request(ROW_NEXT['url'],callback=self.parse_details,meta={'ROW':ROW_NEXT,'Level':0,'No':No_Next},dont_filter=True,headers=self.headers,cookies=self.cookies)
            except:       
                if Level<10:
                    Level+=1                  
                    yield scrapy.Request(response.url,callback=self.parse_reviews,headers=self.headers_json,meta={'ROW':ROW,'Level':Level,'reviews':reviews,'No':No},dont_filter=True)
        else:
            if Level<10:
                Level+=1
                yield scrapy.Request(response.url,callback=self.parse_reviews,headers=self.headers_json,meta={'ROW':ROW,'Level':Level,'reviews':reviews,'No':No},dont_filter=True)
            else:
                print('\n-----------')
                print('OUT: parse_reviews')
    