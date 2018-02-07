"""
Author: Sunil
Date: Jan 27 2018
"""
from datetime import datetime,timedelta
import sys
from time import sleep
from tqdm import tqdm
import random
import os
from bs4 import BeautifulSoup
import requests
import urllib.request

win_unicode_console.enable()

url = "http://www.wsj.com/public/page/archive-"
logfile_path = "E://logfile/logfile.log"

from_date = datetime.strptime(sys.argv[1],"%Y%m%d").date()
to_date = datetime.strptime(sys.argv[2],"%Y%m%d").date()
output_path = sys.argv[3]  # Destination path to store downloaded html pages.
count = int(sys.argv[4])  # Max number of news articles to be downloaded per day.
batch = int(sys.argv[5])  # Batch size of pages to be downloaded in each interval
pause_time = int(sys.argv[6])  # Sleep time in between each batch downloading

delta = to_date - from_date
dates = []
# Generate all dates between from_date and to_date
for i in range(delta.days + 1):
    dates.append(from_date + timedelta(days=i))

wsj_daily_urls = [url+str(each)+".html" for each in dates]
# Log error urls
log_filer = open(logfile_path,'a')

for each in wsj_daily_urls:
# Request page url and read the data.
    output_folder = output_path+"//"+each[-15:-5]
    req_url = requests.get(each).text
    soup = BeautifulSoup(req_url, "lxml")
    article_class = soup.find('ul' , {'class' : 'newsItem'})
    articles_list = article_class.find_all('li')
    url_list = [each.find('h2').find('a',href = True)['href'] for each in articles_list]

    print(">>> Articles to be retrieved for  "+output_folder+ " are  ",len(url_list))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for i in tqdm(range(min(count,len(url_list)))):
        filePath = output_folder+"//" + str(url_list[i].rsplit('/', 1)[1]) + '.html'
        try:
            urllib.request.urlretrieve(url_list[i],filePath)
        except:
           log_filer.write("[error] ",url_list[i])

    # Group URL's in batch size and pause for pause_time +- 10% secs.
    if (i+1) % batch == 0:
        pause_time = pause_time + random.randint(-int(pause_time*0.1), int(pause_time*0.1))
        sleep(pause_time)

#
print(">>>  Downloading Completed")
