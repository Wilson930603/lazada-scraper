BOT_NAME = 'crawldata'
SPIDER_MODULES = ['crawldata.spiders']
NEWSPIDER_MODULE = 'crawldata.spiders'
URLLENGTH_LIMIT = 50000
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOW_ALL=True
TELNETCONSOLE_ENABLED = False
DEFAULT_REQUEST_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept': '*/*','Accept-Language': 'en-GB,en;q=0.5','content-type': 'text/plain','Connection': 'keep-alive','TE': 'trailers',}
ITEM_PIPELINES = {'crawldata.pipelines.CrawldataPipeline': 300}

#pip install scrapy-crawlera
CRAWLERA_APIKEY='9378846f3e314ce99143059b4315a9ba'
CRAWLERA_ENABLED = True
AUTOTHROTTLE_ENABLED = False
CRAWLERA_PRESERVE_DELAY=5

#pip install scrapy_user_agents
RANDOM_UA_PER_PROXY=True
FAKEUSERAGENT_FALLBACK='Mozilla'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy_crawlera.CrawleraMiddleware': 610,
}
LOG_ENABLED = True
LOG_FORMAT = '%(levelname)s: %(message)s'