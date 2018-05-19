import json
import random
import time

import pymysql
import requests

from model import LagouJobInfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_%E5%AE%89%E5%8D%93?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput='
}


def insert_mysql(list_items):
    if len(list_items) == 0:
        print('input data illegal')
        return
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'Mjc19920211',
        'db': 'lagouInfo',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    # Connect to the database
    db = pymysql.connect(**config)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    # data = {
    #     'title': '1',
    #     'address': '2',
    #     'salary': '3',
    #     'workYear': '4',
    #     'company': '5',
    #     'financeStage': '0'
    # }
    table = 'info'
    try:
        for item in list_items:
            data = item.__dict__
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
            # 执行sql语句
            cursor.execute(sql, tuple(data.values()))
            # 提交到数据库执行
        db.commit()

    except Exception as e:
        print('发生错误' + str(e))
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    final_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    # 整体内容进行md5后排重
    set_model = set()

    page_num = 1

    request_args = {'first': 'true', 'pn': '1', 'kd': '安卓'}
    list_item = []
    # 处于简单就爬三页数据
    for i in range(1, 4):
        request_args['pn'] = i
        response = requests.post(final_url, data=request_args, headers=headers)
        time.sleep(random.randint(1, 5))
        json_dict = json.loads(response.text)
        if json_dict['success'] is True:
            content = json_dict['content']
            positionResult = content['positionResult']
            result = positionResult['result']
            for item in result:
                info = LagouJobInfo(item['positionName'], item['stationname'], item['salary'], item['workYear'],
                                    item['companyFullName'], item['financeStage'])
                md5_content = info.get_MD5()
                if md5_content not in set_model:
                    set_model.add(md5_content)
                    list_item.append(info)
                else:
                    print('数据已经存在...' + str(info.__dict__))
        print('finished ' + str(i))
    insert_mysql(list_item)
