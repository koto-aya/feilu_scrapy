# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import pymysql
import pymongo
from .items import *


class NovelSpiderPipeline:
    def dbHandle(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            passwd="root",
            charset="utf8",
            database="xiwu-read"
        )
        return self.conn

    def mongoHandle(self):
        self.client=pymongo.MongoClient("mongodb://admin:fkgrl58791564@8.138.91.116:27017")
        return self.client

    def __del__(self):
        self.conn.close()

    def insertItemToDB(self, item):
        dbObj = self.dbHandle()
        cursor = dbObj.cursor()
        client=self.mongoHandle()
        if isinstance(item, ChapterSpiderItem):
            #获取最新章节id
            cursor.execute("select id from chapter order by id desc limit 1")
            insertSql = "insert into chapter(`id`,`chapter_title`,`novel_id`,`words`) values(%d,'%s','%s','%s')" % (
                item["id"], item["chapter_title"], item["novel_id"], item["words"])
            cursor.execute(insertSql)
        elif isinstance(item, NovelSpiderItem):
            #获取最新小说id
            insertSql = "insert into novel_info(`id`,`title`,`author`,`novel_desc`,`tags`,`imgs_path`,`words`) values(" \
                        "%d,'%s','%s','%s','%s','%s','%s')" % (item["id"], item["title"], item["author"],
                                                               item["novel_desc"], item["tags"], item["imgs_path"],
                                                               item["words"])
            cursor.execute(insertSql)
        elif isinstance(item,ContentSpiderItem):
            db=client["xiwu-read"]
            collection=db["content"]
            data={"cid":item["cid"],"data":item["data"]}
            collection.insert_one(data)
        cursor.connection.commit()
        cursor.close()

    def process_item(self, item, spider):
        self.insertItemToDB(item)
