import codecs
import sys, re, json
import requests
import csv

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

html_tags = {
    'knowledge_panel': 'kp-blk knowledge-panel',
    'claimed': "Own this business?",
    'name': "kno-ecr-pt kno-fb-ctx",
    'phone': 'LrzXr zdqRlf kno-fv',
    'days': "kc:/location/location:hours",
    'address': "kc:/location/location:address"
}

html_regexes = {
    'name': '<span>(.*)</span>',
    'phone': '<span>(.*?)</span>',
    'hours': '<td>(.*)</td>',
    'address': '<span class="LrzXr">(.*)</span>'
}

days = ["Friday","Saturday","Sunday", "Monday","Tuesday","Wednesday", "Thursday"]

def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)
    return r.text

def get_string_after_tag(string, tag, regex, distance):
    if(tag not in string):
        return None

    index = string.find(tag) 
    substr =  string[index:index+distance]
    if re.search(regex,substr):
        return re.search(regex,substr).group(1)
    else:
        return None

def get_details(query):
    html_results = google(query)
    file = codecs.open(r"output.html","w","utf-8")
    file.write(html_results)
    file.close()
    results = {'query':query}
    has_knowledge_panel = html_tags['knowledge_panel'] in html_results

    if(has_knowledge_panel):
        results['exists'] = True
        results['name'] = get_string_after_tag(html_results, html_tags['name'],html_regexes['name'],500)

        results['claimed'] = html_tags['claimed'] not in html_results

        phone_number = get_string_after_tag(html_results, html_tags['phone'],html_regexes['phone'],200)
        if(phone_number):
            results['phone_number'] = phone_number

        address = get_string_after_tag(html_results, html_tags['address'],html_regexes['address'],1000)
        if(address):
            results['address'] = address

        if html_tags['days'] in html_results:
            hours_index = html_results.find(html_tags['days'])
            hours_substr = html_results[hours_index:hours_index+2000]
            for day in days:
                results['{}_hours'.format(day)] = get_string_after_tag(hours_substr,day,html_regexes['hours'],50)
    else:
        results['exists'] = False
    return results


if __name__ == "__main__":
    with open(sys.argv[1], newline='') as csvfile:
        with open('results.csv', 'w', newline='') as results:
            reader = csv.reader(csvfile)
            fieldnames = ['query','exists', 'name','claimed','phone_number','address',
                "Friday_hours","Saturday_hours","Sunday_hours", "Monday_hours","Tuesday_hours","Wednesday_hours", "Thursday_hours"]
            writer = csv.DictWriter(results, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                print(reader.line_num)
                writer.writerow(get_details(u"  ".join(row)))
