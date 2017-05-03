import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup

if __name__ == '__main__':
    driver = webdriver.Chrome("../chromedriver")
    base_url = "http://www.sciencedirect.com/science?_ob=ArticleListURL&_method=list&_ArticleListID=-1193663211&_st=13&filterType=&searchtype=a&originPage=rslt_list&_origin=&_mlktType=&md5=b49ce0803cd7e28acdf036b32ea84e5e"
    driver.get(base_url)
    urls = []
    flag = True
    page = 1
    while flag:
        content = driver.page_source
        page = BeautifulSoup(content)
        if page.find_all('li', 'detail'):
            items = page.find_all('li', 'detail')
            for item in items:
                urls.append(item.a['href'])  
        with open("urls_" + str(page) + ".json", "w") as fp:
            json.dump(urls, fp, indent=4)          
        print (page, "Finished")
        try:
            time.sleep(5)
            driver.find_element_by_name("bottomNext").click()
            time.sleep(5)
            page += 1
        except:
            print ("At the end")
            flag = False

    

