# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sinaCrawler.items import SinacrawlerItem
from scrapy import log


class SinaSpiderSpider(CrawlSpider):
    name = "sina_spider"
    allowed_domains = ["roll.finance.sina.com.cn", "finance.sina.com.cn"]
    start_urls = [r'http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index_' + str(i) + r'.shtml' for i in range(1, 2)]

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        # Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
        Rule(LinkExtractor(
            allow=('http:\/\/finance\.sina\.com\.cn\/stock\/\w+\/\d{4}-\d{2}-\d{2}/doc-\w+\.shtml',)),
            callback='parse_item'),
    )

    def parse_item(self, response):
        log.msg("This is a warning", level=log.INFO)
        item = SinacrawlerItem()
        self.log('Hi, this is an item page! %s' % response.url)
        item['report_url'] = response.url
        item['report_title'] = response.xpath('//*[@id="artibodyTitle"]/text()').extract()[0].replace(' ', '').replace(
            r'\n', '')
        item['report_time'] = response.xpath('//*[@id="wrapOuter"]/div/div[4]/span/text()').extract()[0].replace(' ',
                                                                                                                 '')
        item['report_content'] = ''.join(response.xpath('//*[@id="artibody"]//p/text()').extract()).replace(' ',
                                                                                                            '').replace(
            r'\n', '')

        return item
