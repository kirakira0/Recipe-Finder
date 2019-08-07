import os
import webapp2
import json #lets you parse json files into python directories 
import jinja2
from urllib import urlencode 
from google.appengine.api import urlfetch

# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# the handler section
class SearchFormHandler(webapp2.RequestHandler):
    def get(self): 
        form_template = the_jinja_env.get_template('templates/form.html')
        self.response.write(form_template.render())  # the response 

class RecipePageHandler(webapp2.RequestHandler):
    def post(self):
        
        query = self.request.get('query') #take the value and save it as a python variable 
        base_url = "http://www.recipepuppy.com/api/?" 
        params = {'q':query} #put the query into a parameter list 
        response = urlfetch.fetch(base_url + urlencode(params)).content #fetch a response 
        results = json.loads(response)

        recipe_template = the_jinja_env.get_template('templates/recipe.html')
        self.response.write(recipe_template.render({ #save into a dictionary 
            'results': results
        }))  # the response 

# the app configuration section
app = webapp2.WSGIApplication([
    ('/', SearchFormHandler), #this maps the root url to the Main Page Handler    localhost:8080/form
    ('/recipe', RecipePageHandler)
], debug=True)