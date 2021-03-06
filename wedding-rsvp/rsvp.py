#!/usr/bin/env python

""" Katie's complicated RSVP in web.py 0.3 """
import web
import model
import model_gdata

### Url mappings

urls = (
    '/', 'Index',
    '/rsvp', 'Rsvp',
    '/thanks', 'Thanks'
)


### Templates
render = web.template.render('templates', base='base')
email_render = web.template.render('templates')

familyIdForm = web.form.Form(
  web.form.Textbox('firstName',
    web.form.notnull, description="First Name", class_="text-input"),
  web.form.Textbox('lastName',
    web.form.notnull, description="Last Name", class_="text-input"),
  )

vemail = web.form.regexp(r".*@.*", "must be a valid email address")

mainForm = web.form.Form(
    web.form.Textbox('email', vemail, decription="Email", class_="text-input")
    )

web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'nickandkatie2013@gmail.com'
web.config.smtp_password = 'Password'
web.config.smtp_starttls = True

class Index:
  def GET(self):
    """ Show page """
    form = familyIdForm()
    return render.index(form, True, "", "")

  def POST(self):
    user_data = web.input()

    form = familyIdForm()

    if not form.validates():
      return render.index(form, True, "", "")

    try:
      guest = model.get_guest(user_data.firstName, user_data.lastName)[0]
    except IndexError:
      return render.index(form, False, user_data.firstName, user_data.lastName)
    guests = model.get_guests(guest.partyName)
    
    email_form = mainForm()
    return render.rsvp(guest.partyName, guests, email_form)

class Rsvp:
  def POST(self):
    user_data = web.input()
    email_form = mainForm()

    num_guests = int(user_data.num_guests)

    responses = [ {'partyName': user_data['party_name'],
                   'firstName': user_data['first_name_%d' % guest_num],
                   'lastName': user_data['last_name_%d' % guest_num],
                   'attending': user_data['attending_%d' % guest_num],
                   'mealChoice': user_data['meal_choice_%d' % guest_num],
                   'notes': user_data['notes_%d' % guest_num],
                   'emailAddress': user_data['email']} for guest_num in range(0, num_guests) ]

    if not email_form.validates():
      # ugh, stupid people, we have to go back now...
      guests = model.get_guests(user_data.party_name)
      return render.rsvp(user_data.party_name, responses, email_form)

    yay = False
    for r in responses:
      yay = True if r['attending']=='Yes' else yay


    # shove data into the database
    model.update_guest_responses(responses)

    # shove the responses into google spreadsheet
    model_gdata.update_guest_responses(responses)

    # send an email to the guest to let them know they successfully RSVP-ed
    web.sendmail('nickandkatie2013@gmail.com', user_data['email'], 'Thanks for responding!', email_render.thanks_email(responses, yay), headers={'Content-Type':'text/html;charset=utf-8'})

    # send an email to ourselves
    web.sendmail('nickandkatie2013@gmail.com', 'nickandkatie2013@gmail.com', 'RSVP: %s' % user_data['party_name'], email_render.thanks_email(responses, yay), headers={'Content-Type':'text/html;charset=utf-8'})

    return render.thanks(yay)


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
