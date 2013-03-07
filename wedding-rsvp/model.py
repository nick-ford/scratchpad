import web

db = web.database(dbn='sqlite', db='rsvp.db')

def get_guest(firstName, lastName):
  return db.select('guests', where='firstName=$firstName AND lastName=$lastName', limit=1, vars=locals())

def get_guests(partyName):
  return db.select('guests', where='partyName=$partyName', order='guestOrder', vars=locals())

def update_guest_responses(responses):
  for response in responses:
    db.insert('responses', firstName=response['first_name'],
                           lastName=response['last_name'],
                           attending=('t' if response['attending']=='Yes' else 'f'),
                           mealchoice=response['meal_choice'],
                           notes=response['notes'],
                           email=response['email_address'])
