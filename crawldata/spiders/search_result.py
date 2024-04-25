import scrapy,json,re
from datetime import datetime,timedelta

class CrawlerSpider(scrapy.Spider):
    name = 'search_result'
    #custom_settings={'LOG_FILE':'./log/'+name+'_'+datetime.now().strftime("%Y-%m-%d_%H.%M.%S")+'.log'}
    cookies = {'userLanguageML': 'en'}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-GB,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1','Sec-Fetch-Dest': 'document','Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1','Cache-Control': 'max-age=0',}
    DATE_CRAWL=(datetime.now()+timedelta(1)).strftime('%Y-%m-%d')
    SEARCHRESULTS={'url':'itemUrl','itemId':'itemId','title':'name','image':'image','original_price':'originalPrice','price':'price','discount':'discount','sold_count':'itemSoldCntShow','review_count':'review','rating_score':'ratingScore','seller_id':'sellerId','seller_name':'sellerName','location':'location','brand_name':'brandName'}
    domain='https://www.lazada.co.th'
    lang='en'
    KEYS_CRAWLED=[]
    def __init__(self, lang=None, **kwargs):
        if lang:
            self.lang=str(lang).strip()
            self.cookies['userLanguageML']=lang
        super().__init__(**kwargs)
    def start_requests(self):
        KEYWORDS=re.split('\r\n|\n',open('keywords.txt','r',encoding='utf-8').read())
        for KEYS in KEYWORDS:
            KEY=str(KEYS).split('~')
            if self.lang=='th':
                KEYWORD=KEY[1]
            else:
                KEYWORD=KEY[0]
            KEYWORD=str(KEYWORD).strip()
            if KEYWORD!='' and not KEYWORD in self.KEYS_CRAWLED:
                self.KEYS_CRAWLED.append(KEYWORD)
                url=self.domain+'/catalog/?_keyori=ss&ajax=true&from=input&page=1&q='+(str(KEYWORD).strip()).replace(' ', '+')
                headers={}
                headers.update(self.headers)
                headers['Referer']=str(url).replace('ajax=true&','')
                yield scrapy.Request(url,callback=self.parse_list,meta={'KEYWORD':KEYWORD,'Level':0},headers=headers,dont_filter=True,cookies=self.cookies)
    def parse_list(self, response):
        KEYWORD=response.meta['KEYWORD']
        Level=response.meta['Level']
        if not ('"action":"captcha"' in str(response.text).replace(' ','')) and not('FAIL_SYS_USER_VALIDATE' in response.text):
            DATA=json.loads(response.text)
            for row in DATA['mods']['listItems']:
                item={}
                item['keyword']=KEYWORD
                for k,v in self.SEARCHRESULTS.items():
                    if v in row:
                        item[k]=row[v]
                    else:
                        item[k]=''
                if str(item['url']).startswith('//'):
                    item['url']='https:'+item['url']
                yield(item)
            PAGE=DATA['mainInfo']
            if int(PAGE['page'])*int(PAGE['pageSize'])<int(PAGE['totalResults']):
                Page=int(PAGE['page'])+1
                url=self.domain+'/catalog/?_keyori=ss&ajax=true&from=input&page='+str(Page)+'&q='+KEYWORD
                yield scrapy.Request(url,callback=self.parse_list,dont_filter=True,meta={'KEYWORD':KEYWORD,'Level':0},headers=self.headers,cookies=self.cookies)
        else:
            if Level<10:
                Level+=1
                yield scrapy.Request(response.url,callback=self.parse_list,meta={'KEYWORD':KEYWORD,'Level':Level},headers=self.headers,dont_filter=True,cookies=self.cookies)