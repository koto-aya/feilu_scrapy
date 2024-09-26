# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelSpiderItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    novel_desc = scrapy.Field()
    tags = scrapy.Field()
    imgs_path = scrapy.Field()
    words = scrapy.Field()


class ChapterSpiderItem(scrapy.Item):
    id = scrapy.Field()
    chapter_title = scrapy.Field()
    novel_id = scrapy.Field()
    words = scrapy.Field()


class ContentSpiderItem(scrapy.Item):
    cid = scrapy.Field()
    data = scrapy.Field()
