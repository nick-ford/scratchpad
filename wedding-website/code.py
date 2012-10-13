import web
render = web.template.render('templates/')

urls = (
    '/', 'index'
)

class section:
  def __init__(self, section_name, image_name, image_size_class, caption):
    self.section_name = section_name
    self.image_name = image_name
    self.image_size_class = image_size_class
    self.caption = caption


sections = [
    section("Events", "event.jpg", "size-event", "Events"),
    section("Attractions", "attractions.jpg", "size-attractions", "Attractions"),
    section("Maps", "maps.jpg", "size-2", "Maps"),
    section("Accomodations", "accomodations.jpg", "size-3", "Accomodations"),
    section("Registry", "registry.jpg", "size-2", "Registry")]

class index:
    def GET(self):
        #return "Hello, world!"
        #i = web.input(name=None)
        return render.index(sections)
        #return render.index()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
