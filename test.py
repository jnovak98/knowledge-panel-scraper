import codecs
import sys, re, json
import requests
from bs4 import BeautifulSoup

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

days = ["Friday","Saturday","Sunday", "Monday","Tuesday","Wednesday", "Thursday"]

def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)
    return r.text
    soup = BeautifulSoup(r.text, "html.parser")
    output = []
    for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
        url = searchWrapper.find('a')["href"]
        text = searchWrapper.find('a').text.strip()
        result = {'text': text, 'url': url}
        output.append(result)

    return output

if __name__ == "__main__":
    s = google(sys.argv[1])
    knowledge_panel_string = 'kp-blk knowledge-panel EyBRub Wnoohf OJXvsb'
    claimed_string = "Own this business?"
    exists = knowledge_panel_string in s
    claimed = not claimed_string in s
    name_html = "kno-ecr-pt kno-fb-ctx PZPZlf gsmt"
    name_index = s.find(name_html)
    name_surrounding = s[name_index:name_index+500]
    name = re.search('<span>(.*)</span>',name_surrounding).group(1)

    days_html = "kc:/location/location:hours"
    days_index = s.find(days_html)
    days_surrounding = s[days_index:days_index+2000]
    hours = {}
    for day in days:
        date_index = days_surrounding.find(day)
        date_surrounding = days_surrounding[date_index:date_index+40]
        hours[day] = re.search('<td>(.*)</td>',date_surrounding).group(1)

    print("{0}   {1}   {2}    {3}".format(exists,claimed,name,json.dumps(hours)))
    file = codecs.open(r"output","w","utf-8")
    file.write(s)
    file.close
