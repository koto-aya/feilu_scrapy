import requests
import scrapy
from lxml import etree
from scrapy.downloadermiddlewares import stats

from ..items import *
from .. import aliyun_util
from ..utils.dbutil import DBUtils

class NovelSpider(scrapy.Spider):
    name = "novel"
    allowed_domains = ["b.faloo.com"]
    start_urls = ["https://b.faloo.com/1438715.html"]

    def parse_xml(self, html, xml_expression: str, only_one=True):
        data = html.xpath(xml_expression)
        if only_one: return data[0]
        return data

    def parse_chapter(self, response):
        body = response.body
        html = etree.HTML(body)
        chapter_item = ChapterSpiderItem()
        dbutil = DBUtils()
        content_item=ContentSpiderItem()
        # 小说id
        novel_id = response.meta["novel_id"]
        # 章节标题
        # 原标题格式：封神天兵：从掠夺词条开始崛起！   第三十八章 昊天召见，天帝威仪！
        chapter_title: str = self.parse_xml(html, "//div[@class='WallPageBody']/div[@class='c_l_title']/h1/text()")
        chapter_title = chapter_title.split("！   ")[1]
        # 章节内容
        contents = self.parse_xml(html, "//div[@class='WallPageBody']/div[@class='noveContent']/p/text()", False)
        data = ""
        for content in contents:
            data += content + "\\n"
        # 统计字数
        words = len(data)
        chapter_item["id"]=dbutil.get_last_chapter_id()
        chapter_item['novel_id'] = novel_id
        chapter_item['chapter_title'] = chapter_title
        chapter_item['words'] = words
        # 插入章节信息
        yield chapter_item
        #插入小说内容信息
        content_item["cid"]=chapter_item["id"]
        content_item["data"]=data
        yield content_item

    def parse(self, response):
        body = response.body
        html = etree.HTML(body)
        dbutil=DBUtils()
        novel_info = NovelSpiderItem()

        novel_info["id"]=dbutil.get_last_novel_id()
        novel_info["title"] = self.parse_xml(html=html, xml_expression="//div[@class='T-L-O-Z-Box1']/h1/text()")
        novel_info["author"] = self.parse_xml(html, "//div[@class='T-L-O-Z-Box1']/a/@title")
        # 获取小说简介
        contents = self.parse_xml(html, "//div[@class='T-L-T-Content']/div[@class='T-L-T-C-Box1']/p/text()", False)
        desc = ""
        for content in contents:
            desc += content + "\\n"
        novel_info["novel_desc"] = desc
        # 获取小说标签
        novel_info["tags"] = self.parse_xml(html,
                                            "//div[@class='Two-Right']/div[@class='T-R-Top']/div[@class='T-R-T-Box2']/div[@class='T-R-T-B2-Box1']/a[@class='LXbq']/text()")
        # 获取小说图片并上传aliyun的oss
        download_addr = self.parse_xml(html, "//div[@class='T-L-Two']/div[@class='T-L-T-Img']/a/img/@src")
        data = requests.get(download_addr)
        access_path = aliyun_util.upload(data)
        novel_info["imgs_path"] = access_path
        # 获取小说字数，以万字为单位
        words = self.parse_xml(html,
                               "//div[@class='Two-Right']/div[@class='T-R-Middle2']/ul/li[2]/div[@class='zi2']/text()")
        novel_info["words"] = words
        yield novel_info

        # 爬取章节数据
        body = response.body
        html = etree.HTML(body)
        chapters = self.parse_xml(html,
                                  "//div[@class='C-Fo-Zuo']//div[@class='DivTable']/div[@class='DivTr']/div[@class='DivTd3']",
                                  False)
        for chapter in chapters:
            href = self.parse_xml(chapter, "a/@href")
            href = "https:" + href
            yield scrapy.Request(url=href, callback=self.parse_chapter, meta={"novel_id": novel_info["id"]})
