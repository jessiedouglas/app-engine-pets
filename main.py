#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))
    
    
class Pet(ndb.Model):
    name = ndb.StringProperty()
    animal_type = ndb.StringProperty()
    breed = ndb.StringProperty()
    age = ndb.IntegerProperty()
    

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/pet_questionaire.html')
        self.response.write(template.render())
        
    def post(self):
        name = self.request.get('name')
        animal_type = self.request.get('type')
        breed = self.request.get('breed')
        age = int(self.request.get('age'))
        
        new_pet = Pet(name=name, animal_type=animal_type, breed=breed, age=age)
        new_pet.put()
        
        template_variables = {
            'name': name,
            'animal_type': animal_type,
            'breed': breed,
            'age': age
        }
        template = jinja_environment.get_template('templates/pet_answers.html')
        self.response.write(template.render(template_variables))
        

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
