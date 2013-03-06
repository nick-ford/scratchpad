import web
import urllib
import urllib2

def update_guest_response(party_name, first_name, last_name, attending, meal_choice, email_address, notes=''):
  form_url = 'https://docs.google.com/forms/d/1gV5jWp8EsqJCpUyyIj5N4LT5bXmURRkiCExATHLEQQw/formResponse'

  # TODO: some value checking here
  values = {'entry.213675741' : party_name,
            'entry.1888509213': first_name,
            'entry.1297331898' : last_name,
            'entry.413708656' : attending,
            'entry.398827781' : meal_choice,
            'entry.1816148762' : notes,
            'entry.400474913' : email_address}

  data = urllib.urlencode(values)
  req = urllib2.Request(form_url, data)
  response = urllib2.urlopen(req)
  # TODO: some checking here
  the_page = response.read()

