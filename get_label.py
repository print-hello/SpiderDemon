'''
Author: Vinter Wang
爬取所有a标签
'''
import requests
from bs4 import BeautifulSoup
import pymysql
import datetime


def get_label():
    conn = pymysql.connect(host='localhost', port=3306,
        user='root', password='******',
        db='link2', charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    } 
    link_list = get_link(conn)
    domain_list = get_domain(conn)
    for url in link_list:
        print(url)
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        label_list = soup.find_all('a')
        href_list = []
        for each in label_list:
            try:
                each_process = each.get('href').split('/')[2].lstrip('www.')
                href_list.append(each_process)
            except:
                pass
        uniq_href_list = list((set(href_list)))
        for uniq_href in uniq_href_list:
            if uniq_href in domain_list:
                write_db(conn, url, 1)
                print(uniq_href)    
                break
            else:
                write_db(conn, url)

def get_domain(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT domain from li_post_domian_reference')
    results = cursor.fetchall()
    domain_list = []
    for res in results:
        domain = res['domain']
        domain_list.append(domain)
    cursor.close()
    return domain_list

def write_db(conn, url, state=0):
    spider_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    if state == 0:
        cursor.execute('UPDATE li_result set spider_time="%s" where link="%s"' % (spider_time, url))
    elif state == 1:
        cursor.execute('UPDATE li_result set status=1, spider_time="%s" where link="%s"' % (spider_time, url))
    conn.commit()
    cursor.close()

def get_link(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT link from li_result')
    results = cursor.fetchall()
    link_list = []
    for res in results:
        link = res['link']
        link_list.append(link)
    cursor.close()
    return link_list


if __name__ == '__main__':
    get_label()