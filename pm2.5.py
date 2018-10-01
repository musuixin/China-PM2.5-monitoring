import requests
import webbrowser
from pyecharts import Geo, Page
from bs4 import BeautifulSoup
import re
import datetime

url = "http://www.86pm25.com/paiming.htm"
head = {
    'Referer': 'http://www.86pm25.com/city/Dazhou.html',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
html = requests.get(url, headers=head)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, "lxml")
data1 = soup.find(id="goodtable").find_all(name='a')
data2 = str(soup.find(id='goodtable').find_all(name='td'))
data = re.findall(r'<td>(\d{1,3}.)</td>', data2)
with open("城市.txt", 'r') as f:
    CityList = f.read()
city = []
for i in range(0, 367):
    if str(data1[i].string) in CityList:
        citytuple = (data1[i].string, int(data[i]))
        city.append(citytuple)
geo = Geo("全国主要城市空气质量实时监控", "实时：" + str(datetime.datetime.now()), title_color="#fff",
          title_pos="center", width='100%',
          height=790, background_color='#404a59')
attr, value = geo.cast(city)
geo.add("", attr, value, visual_range=[0, 150], maptype='china', visual_text_color="#fff",
        symbol_size=13, is_visualmap=True)
page = Page()
page.add(geo)
page.render("全国主要城市空气质量实时监控.html")
webbrowser.open("全国主要城市空气质量实时监控.html", new=0, autoraise=True)
