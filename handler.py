import os
import json
import time
import csv
from config import resultFile

if not os.path.exists('./dist'):
    os.mkdir('./dist')
    
f = open(f'./dist/{resultFile}', mode='w' , encoding='utf-8')
writer = csv.writer(f)
writer.writerow(['title', 'link', 'cover', 'update', 'read_num', 'like_num'])

def onArticleList(res) -> bool:
    data = json.loads(res)
    if not data["base_resp"]["ret"] == 0:
        raise 'article list res error'

    publish_page = json.loads(data["publish_page"])
    if not publish_page:
        return True
    
    publish_list = publish_page["publish_list"]
    
    if not publish_list or not len(publish_list):
        return True

    for item in publish_list:
        infoStr = item["publish_info"]
        if not infoStr:
            continue
        publish_info = json.loads(infoStr)
        appmsgex = publish_info["appmsgex"]
        if appmsgex and len(appmsgex):
            title = appmsgex[0]["title"]
            link = appmsgex[0]["link"]
            cover = appmsgex[0]["cover"]
            update = appmsgex[0]["update_time"]
            updateString = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(update))
            [read_num, like_num] = [0, 0]
            writer.writerow([title, link, cover, updateString, read_num, like_num])
            f.flush()
        