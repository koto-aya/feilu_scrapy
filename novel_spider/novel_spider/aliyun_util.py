# -*- coding: utf-8 -*-
import oss2
import configparser
import datetime
import uuid
# 读取配置文件
config = configparser.ConfigParser()
# 假设config.ini位于脚本同级目录下
config.read('novel_spider/config.ini')

# 从配置文件中获取Access Key ID和Access Key Secret
access_key_id = config.get('configName', 'alibaba_cloud_access_key_id')
access_key_secret = config.get('configName', 'alibaba_cloud_access_key_secret')

# 使用获取的RAM用户的访问密钥配置访问凭证
auth = oss2.AuthV4(access_key_id, access_key_secret)
# 使用auth进行后续操作...
base_save_url="https://xy-read.oss-cn-fuzhou.aliyuncs.com/"
def upload(data):
    today = datetime.datetime.today()
    year = today.year.__str__()
    month = today.month
    if month<10:
        month="0"+month.__str__()
    name=uuid.uuid4().__str__()
    upload_path=year+"/"+month+"/"+name+".jpg"
    # 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # yourBucketName填写存储空间名称。
    bucket = oss2.Bucket(auth, 'https://oss-cn-fuzhou.aliyuncs.com', 'xw-read',region="cn-fuzhou")
    # 上传文件到OSS。
    # yourObjectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
    # yourLocalFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    bucket.put_object(upload_path, data)
    return base_save_url+upload_path