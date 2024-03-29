import os
import webapp2
import json #lets you parse json files into python directories 
import jinja2
from urllib import urlencode 
from google.appengine.api import urlfetch
# from pprint import pprint
import pprint

import logging


# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# the handler section
class SearchFormHandler(webapp2.RequestHandler):
    def get(self): 
        print("GET")
        logging.debug("some helpful debug info")

        form_template = the_jinja_env.get_template('templates/form.html')
        self.response.write(form_template.render())  # the response 

class RecipePageHandler(webapp2.RequestHandler):
    def post(self):
        print("POST")
        logging.debug("some helpful debug info")

        
        query = self.request.get('query') #take the value and save it as a python variable 
        ingredients = self.request.get('ingredients')
        base_url = "http://www.recipepuppy.com/api/?" 

        logging.debug("INGREDIENTS: " + ingredients)

        params = {'q':query, 'i':ingredients} #put the query into a parameter list 

        api_url = base_url + urlencode(params)
        logging.debug("API URL: " + api_url)

        response = urlfetch.fetch(api_url).content #fetch a response 
        results = json.loads(response)
        # pprint(results)
        # logging.debug(pprint.pformat(results))


        recipe_template = the_jinja_env.get_template('templates/recipe.html')
        self.response.write(recipe_template.render({ #save into a dictionary 
            'results': results
        }))  # the response 

# the app configuration section
app = webapp2.WSGIApplication([
    ('/', SearchFormHandler), #this maps the root url to the Main Page Handler    localhost:8080/form
    ('/recipe', RecipePageHandler)
], debug=True)