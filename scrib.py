#encoding=utf8
import urllib2
from bs4 import BeautifulSoup
import bs4
import time
import MySQLdb
import sys

print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf8')

page=1
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
data_base={}
count=0

def retriveJokes():
    global page
    try:
        url = 'http://www.qiushibaike.com/hot/page/' + str(page)
        request=urllib2.Request(url,headers=headers)
        response=urllib2.urlopen(request)
        html=response.read().decode('utf-8')
        soup=BeautifulSoup(html,"lxml")
        contents=soup.find(id='content-left')
        for item in contents.children:
            if isinstance(item,bs4.element.Tag) and item.name=='div' and None==item.find('div',class_='thumb'):
                joke=item.find('div',class_='content').get_text()
                if(len(joke)<100):
                    data_base[item['id']]=joke
    except urllib2.URLError,e:
        if hasattr(e,'code'):
            print e.code
        if hasattr(e,"reason"):
            print e.reason

def persistance():
    global count
    list=[]


    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='world', port=3306,charset='utf8')

    cur = conn.cursor()
    cur.execute("select count(1) from t_jokes")
    count=cur.fetchone()[0]
    for key in data_base.keys():
        data = data_base.get(key)
        list.append((count, key, data.strip()))
        count = count + 1

    cur.executemany('insert into t_jokes (id,itemid,content) values(%s,%s,%s)', list)
    conn.commit()
    cur.close()
    conn.close()
    print 'count#'+str(count)
    data_base.clear()





if __name__ =="__main__":
    while(True):
        print "page#"+str(page)
        retriveJokes()
        persistance()
        page=page+1
        time.sleep(1)
        if(count>1000):
            break

