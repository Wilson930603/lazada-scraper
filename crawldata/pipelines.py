import json
from datetime import datetime

class CrawldataPipeline:
    def open_spider(self, spider):
        file_name = f'./Data/{spider.name}_{spider.lang}_{datetime.now().strftime("%Y-%m-%d_%H.%M.%S")}'
        self.data_file_name = file_name + '.json'
        self.DATASET=[]

    def close_spider(self, spider):
        if len(self.DATASET)>0:
            data_file = open(self.data_file_name, 'w', encoding='utf-8')
            data_file.write(json.dumps(self.DATASET))
            data_file.close()

    def process_item(self, item, spider):
        self.DATASET.append(item)
        #return item