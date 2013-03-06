import web

db = web.database(dbn='sqlite', db='rsvp.db')

def get_guest(firstName, lastName):
  return db.select('guests', where='firstName=$firstName AND lastName=$lastName', limit=1, vars=locals())

def get_guests(partyName):
  return db.select('guests', where='partyName=$partyName', order='guestOrder', vars=locals())

def update_guest_response(first_name, last_name, attendance, meal_choice, email_address, food_notes=''):

  db.insert('responses', firstName=first_name,
                         lastName=last_name,
                         attending=('t' if attendance=='Yes' else 'f'),
                         mealchoice=meal_choice,
                         notes=food_notes,
                         email=email_address)



