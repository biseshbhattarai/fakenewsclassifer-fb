import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import json 


class Scraper : 
    
    def __init__(self):
        self.page = 15 

    def scrape_onlinekhabar(self):
        for page_number in range(0,int(self.page)):
            sauce = requests.get('https://www.onlinekhabar.com/content/news/page'+str(page_number))
            soup = BeautifulSoup(sauce.text,'lxml')
            posts = soup.find_all("div",class_="relative list__post show_grid--view")
            for post in posts:
                wrapper = post.find_all("div",class_="item")
                tag = wrapper[-1].find('a')
                title = tag.text
                link = tag['href']
                source = link.split('/')[2]
                print(title)
                with open('online_khabar.txt','a') as fq:
                    fq.write(title+"\n")


    def scrape_nagarik(self):
    	for page_number in range(0,int(self.page)): 
            sauce = requests.get('https://nagariknews.nagariknetwork.com/category/21?page='+str(page_number))
            soup = BeautifulSoup(sauce.text,'lxml')
            if page_number == 1:
                data = soup.find_all("div",class_="col-sm-3 part-ent")
                for d in data:
                    with open('nagarik_news.txt','a') as csv_file:
                        title = d.find('a').text
                        link = "https://nagariknews.nagariknetwork.com" +d.find('a')['href']
                        print(title+'\n'+link)
                        csv_writer = csv.writer(csv_file,delimiter=',')
                        csv_writer.writerow([title,link,"https://nagariknews.nagariknetwork.com"])
            else:
                posts = soup.find_all('div',class_="col-sm-9 detail-on")
                for data in posts:
                    with open('nagarik_news.txt','a') as csv_file:
                        title = data.find('a').text
                       	csv_file.write(title)

    def scrape_kantipur(self):
        i=0 
        day = datetime.today()
        for _ in range(3):         
                url = "https://www.kantipurdaily.com/news/"+str(day)[:10].replace('-','/')+"?json=true"
      
                day = day - timedelta(days=1)
                r = requests.get(url)
         
                p = BeautifulSoup(json.loads(r.text)["html"],"lxml")
                posts = p.find_all("h2")
                for title in posts:
                        data = title.find("a")
                        with open("kantipur_daily.txt",'a') as csv_file:
                                csv_file.write(data+'\n')
                              
                               
       
    
    def scrape_annapurnapost(self):
        for number in range(1,5):
            resp = requests.get("http://bg.annapurnapost.com/api/news/list?page=0&per_page="+str(number)+"&category_alias=politics&isCategoryPage=1")
            p = json.loads(resp.text)
            data = p["data"]
            for post in data:
                    title = post["title"]
                    link = url+str(post["id"])
                    print(link)
                    with open("annapurna_post.txt",'a') as csv_file:
                            csv_file = csv.writer(csv_file,delimiter=',')
                            csv_file.writerow([title,link,"AnnapurnaPost"])


scrape = Scraper()
scrape.scrape_onlinekhabar()
