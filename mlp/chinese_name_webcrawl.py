import requests
import re
from bs4 import BeautifulSoup as bs

def getHTML(url, headers=None):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.content
    else:
        print(f'【{url}】 is not working!')
        return False

def getMetaData(url, headers=None):
    html = getHTML(url, headers=headers)
    if html:
        soup = bs(html, 'lxml')
        names = soup.select('body > div.main_ > div > div > div > a')
        lastNames = []
        counts = []
        links = []
        for name in names:
            ln = re.search(r'.+(?=姓名字大全)', name.string)
            lastNames.append(ln.group())
            cts = re.search(r'\d+', name['title']).group()
            counts.append(int(cts))
            links.append('https://www.resgain.net/' + name['href'])
        return lastNames, counts, links        

def getNameLinksByGender(lname_link):
    boy_links = [lname_link + '&gender=1']
    girl_links = [lname_link + '&gender=0']
    return boy_links, girl_links

def getFullNames(urls, headers=None):
    fullnames = []
    for url in urls:
        html = getHTML(url, headers=headers)
        if html:
            soup = bs(html, 'lxml')
            names = soup.select('body > div.main_ > div > div > div > div')
            fullnames.extend([name.text.strip() for name in names[:-1]])
    return fullnames

def getFirstNames(fullName, lastName):
    firstName = lambda fullName, lastName: fullName[len(lastName):]
    if isinstance(fullName, list):
        return list(map(firstName, fullName, [lastName] * len(fullName)))
    elif isinstance(fullName, str):
        return firstName(fullName, lastName)
    else:
        raise ValueError('fullName should be either list or str')

def nameInfoWriter(lname, lname_link, writer, template):
    boy_links, girl_links = getNameLinksByGender(lname_link)
    boy_fullnames = getFullNames(boy_links)
    boy_firstnames = getFirstNames(boy_fullnames, lname)
    girl_fullnames = getFullNames(girl_links)
    girl_firstnames = getFirstNames(girl_fullnames, lname)
    
    for i in range(len(boy_fullnames)):
        writer.write('\n')
        writer.write(template.format(lname, boy_firstnames[i], boy_fullnames[i], 'M'))
    for i in range(len(girl_fullnames)):
        writer.write('\n')
        writer.write(template.format(lname, girl_firstnames[i], girl_fullnames[i], 'F'))
    print(f'Finish writing name info related to {lname}...')

url = 'http://www.resgain.net/xmdq.html'
lastNames, counts, links = getMetaData(url)

with open('中国人名信息库.txt', 'w') as f:
    template = '{}\t{}\t{}\t{}'
    f.write(template.format('姓', '名', '全名', '性别'))
    for i in range(len(lastNames)):
        nameInfoWriter(lastNames[i], links[i], f, template)

with open('元数据.txt', 'w') as f:
    template = '{}\t{}\t{}'
    f.write(template.format('姓', '姓名数', '链接'))
    for i in range(len(lastNames)):
        f.write('\n')
        f.write(template.format(lastNames[i], counts[i], links[i]))