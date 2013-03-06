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

familyIdForm = web.form.Form(
  web.form.Textbox('firstName',
    web.form.notnull, description="First Name"),
  web.form.Textbox('lastName',
    web.form.notnull, description="Last Name"),
  )

vemail = web.form.regexp(r".*@.*", "must be a valid email address")

mainForm = web.form.Form(
    web.form.Textbox('email', vemail, decription="Email")
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

    if not email_form.validates():
      # ugh, stupid people, we have to go back now...
      guests = model.get_guests(user_data.party_name)
      return render.rsvp(user_data.party_name, guests, email_form)

    num_guests = int(user_data.num_guests)

    for guest_num in range(0, num_guests):
      model_gdata.update_guest_response(party_name = user_data['party_name'],
                                  first_name = user_data['first_name_%d' % guest_num],
                                  last_name = user_data['last_name_%d' % guest_num],
                                  attending = user_data['attending_%d' % guest_num],
                                  meal_choice = user_data['meal_choice_%d' % guest_num],
                                  notes = user_data['notes_%d' % guest_num],
                                  email_address = user_data['email'])

      model.update_guest_response( first_name = user_data['first_name_%d' % guest_num],
                                   last_name = user_data['last_name_%d' % guest_num],
                                   attendance = user_data['attending_%d' % guest_num],
                                   meal_choice = user_data['meal_choice_%d' % guest_num],
                                   food_notes = user_data['notes_%d' % guest_num],
                                   email_address = user_data['email'])


    web.sendmail('nickandkatie2013@gmail.com', user_data['email'], 'Thanks for the RSVP!', 'Here is a summary:')
    return render.thanks()



app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
