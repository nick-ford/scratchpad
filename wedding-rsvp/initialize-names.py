import sqlite3

import gdata.spreadsheet.service
import gdata.service
import string

def guest_generator():
  # get the name feed
  gd_client = gdata.spreadsheet.service.SpreadsheetsService()
  gd_client.email = 'nickandkatie2013@gmail.com'
  gd_client.password = 'Password'
  gd_client.source = 'Wedding List Initializer'
  gd_client.ProgrammaticLogin()

  sheetkey = 'ty2aEMZNQ8Nv5m8Wm0EhruQ'
  worksheet_id = 'od6'

  feed = gd_client.GetListFeed(sheetkey, worksheet_id)

  for i, entry in enumerate(feed.entry):
    firstName = entry.custom['firstname'].text.strip()
    lastName = entry.custom['lastname'].text.strip()
    partyName = entry.custom['partyname'].text.strip()
    guestOrder = entry.custom['guestorder'].text.strip()

    yield (partyName, guestOrder, firstName, lastName)

conn = sqlite3.connect('rsvp.db')
c = conn.cursor()
c.executemany('INSERT INTO guests(partyName, guestOrder, firstName, lastName) VALUES (?,?,?,?)', guest_generator())

conn.commit()
conn.close()
