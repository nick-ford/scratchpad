import urllib
import urllib2

url = "https://docs.google.com/forms/d/1gV5jWp8EsqJCpUyyIj5N4LT5bXmURRkiCExATHLEQQw/formResponse"
values = {'entry.213675741' : '1',
          'entry.1888509213' : 'Katie Webb',
          'entry.398827781' : 'Chicken'}
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()

print (the_page)
