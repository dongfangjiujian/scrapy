import scrapy
from ..items import LoveFouItem

class LoveFou(scrapy.Spider):
    name = 'lovefou'

    start_urls=["https://www.xlovefou.com/shijie/"]

    def parse(self, response):
        category_list = response.xpath('//li[@id="long"]/a/@href').extract()
        for c in category_list:
            url = response.urljoin(c)
            yield scrapy.Request(url,callback=self.getPic)

        next_page = response.xpath('//div[@class="pagination"]/ul/a[last()-1]/@href').extract_first()
        if next_page:
            next_url =response.urljoin(next_page)
            print("这是下一页的地址："+next_url)
            yield scrapy.Request(next_url,callback=self.parse)

    def getPic(self,response):
        img_url = response.xpath('//div[@class="conmmtu"]/p/a/img/@src').extract_first()
        img_name=response.xpath('//div[@class="title"]/h1/text()').extract_first()
        category_name=img_name.split('(')[0]
        item=LoveFouItem()
        item['image_name']=img_name
        item['image_url']=img_url
        item['category_name']=category_name
        yield item
        next_page=response.xpath('//div[@class="pageturn"]/a[last()]/@href').extract_first()
        next_category=response.xpath('//div[@class="pagelast"]/p/a[last()]/@href').extract_first()
        if next_page is not None:
            next_url=response.urljoin(next_page)
        else:
            next_url=response.urljoin(next_category)
        yield scrapy.Request(next_url,callback=self.getPic)


