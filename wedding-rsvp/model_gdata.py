import web
import urllib
import urllib2

def update_guest_responses(responses):
  form_url = 'https://docs.google.com/forms/d/1gV5jWp8EsqJCpUyyIj5N4LT5bXmURRkiCExATHLEQQw/formResponse'

  for response in responses:
    values = {'entry.213675741' : response['partyName'],
              'entry.1888509213': response['firstName'],
              'entry.1297331898' : response['lastName'],
              'entry.413708656' : response['attending'],
              'entry.398827781' : response['mealChoice'],
              'entry.1816148762' : response['notes'],
              'entry.400474913' : response['emailAddress']}

    data = urllib.urlencode(values)
    req = urllib2.Request(form_url, data)
    response = urllib2.urlopen(req)
    # TODO: some checking here
    the_page = response.read()

