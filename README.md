# Thai scraping project

## Project consists of 2 parts:
1- Scrape Lazada.co.th for some of search keywords listed in search_words.txt file and save result products info & product_url to json file label starts with search_result.

2- Scrape Lazada.co.th for list of product URLs from above output file and save result products info to json file label starts with product_detail.

## Installation:
To run this project you need python (version>=3.8) installed a long with scrapy framework.
Download and install python using https://www.python.org/downloads.

Install prerequisite libraries from requirements.txt file,
  Navigate to project directory and run:
```bash
pip install -r requirements.txt
```

## Install keywords list to search
Open keywords.txt file and add keyword list base line
Structure:
```bash 
keyword_en~keyword_th 
```

## Run spider:
Open a terminal or command prompt and navigate to the directory where the project is saved,

Run search spider:
```bash
scrapy crawl search_result -a lang=xx
```
xx=en: use keyword_en (English) to search

xx=th: use keyword_th (Thailand) to search

Results will export to json data file in ./Data folder; file is search_result_lang_YYYY-MM-DD_HH.MM.SS.json

The spider will start scraping and search website

and save the extracted data / URLs in a JSON file.

Run scrape product urls spider:

#### Get product_detail with full reviews
```bash
scrapy crawl product_detail
```
#### Get product_detail with the number of reviews as parameter
```bash
scrapy crawl product_detail -a reviews=x
```
x: is the reviews number want to get (interger)

Spider will list all search_result data files:

0 - search_result ...

1 - search_result ...

Need input the rank number of list to get product detail base on the list crawled.

#### Input the number of file will get detail: x

Press Enter to start crawl data

### Project structure
- scrapy_project directory: contains scrapy project configuration files (setting.py, pipeline.py, ...)
- spiders directory: contains project spiders one Class for each project part:
  - search_result
  - product_detail  
- output directory: contains output JSON files.
- logs directory: contains spiders log files.
- crawlera_api contains is CRAWLERA_APIKEY=xxxx in the settings.py

Output:
Expected JSON output tables
location: Data/spider_name_lang_YYYY-MM-DD_HH.MM.SS.json
