# -*- coding: utf-8 -*-
import scrapy
import json
from images360.items import Images360Item
from urllib.parse import urlencode


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zj?'
        for i in range(1, self.settings.get('MAX_PAGE')+1):
            sn = i*30
            data['sn'] = sn
            params = urlencode(data)
            url = base_url + params
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        content = json.loads(response.text)
        for image in content['list']:
            item = Images360Item()
            item['id'] = image['imageid']
            item['url'] = image['qhimg_url']
            item['title'] = image['group_title']
            item['thumb'] = image['qhimg_thumb_url']
            yield item
