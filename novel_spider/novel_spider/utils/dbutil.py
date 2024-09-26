import pymysql


class DBUtils:
    def dbHandle(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            passwd="root",
            charset="utf8",
            database="xiwu-read"
        )
        return self.conn

    def get_last_novel_id(self):
        conn = self.dbHandle()
        cursor=conn.cursor()
        cursor.execute("select * from novel_info order by id desc limit 1")
        id=cursor.fetchone()[0]+1
        cursor.close()
        conn.close()
        return id


    def get_last_chapter_id(self):
        conn = self.dbHandle()
        cursor = conn.cursor()
        cursor.execute("select * from chapter order by id desc limit 1")
        id=cursor.fetchone()[0]+1
        cursor.close()
        conn.close()
        return id
