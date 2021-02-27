import os
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'https://nx0084.tistory.com'
html = requests.get(url).text

soup =BeautifulSoup(html,'html.parser')

category_list = soup.select('ul>li>a.link_sub_item')

for link in category_list:
    category_url = url +link.get('href')
    pageNum = 1

    while True:

        cur_category_url = category_url + '?page='+str(pageNum)
        category_html = requests.get(cur_category_url).text

        soup = BeautifulSoup(category_html,'html.parser')
        content_link_list = soup.select('div.post-item>a')

        if content_link_list.__len__()==0:
            break

        for content_link in content_link_list:

            content_link_href = content_link.get('href')
            content_html = requests.get(url+content_link_href).text

            soup = BeautifulSoup(content_html,'html.parser')
            title = soup.select('h1')[1]

            if not (os.path.isdir('./'+title.get_text())):
                os.mkdir('./'+title.get_text())

            print(title.get_text() + "추출중")

            content_img_list = soup.select('img[srcset]')
            n=1
            for content_img in content_img_list:
                imgUrl = content_img.get('srcset')
                with urlopen(imgUrl) as f:
                    with open('./'+title.get_text().rstrip()+'/ '+str(n)+'.jpg', 'wb') as h:
                        img = f.read()
                        h.write(img)

                n+=1

        pageNum+=1