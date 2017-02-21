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
import cgi
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

#Creates object to interface with database
class Blogs(db.Model):
    title = db.StringProperty(required=True)
    body= db.StringProperty(required=True, multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

#get 5 recent blog posts from database
#def retrieveBlog(database):
 #   blogs = db.GqlQuery("SELECT * FROM database ORDER BY created DESC LIMIT 5")
 #   return blogs

class MainHandler(webapp2.RequestHandler):
    def get(self):
       blogs = db.GqlQuery("SELECT * FROM Blogs ORDER BY created DESC LIMIT 5")
       t = jinja_env.get_template("mainBlog.html")
       content = t.render(blogs = blogs)
       self.response.write(content)

class NewPostHandler(webapp2.RequestHandler):
   def get(self):
       t = jinja_env.get_template("newPost.html")
       content = t.render()
       self.response.write(content)


class BlogHandler(webapp2.RequestHandler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blogs ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("mainBlog.html")
        content = t.render(blogs=blogs)
        self.response.write(content)

    def post(self):
        error = ""
        title = self.request.get("title")
        body = self.request.get("entry")
        if (not title) or (title.strip() == "") and (not body) or (body.strip() == ""):
            error = "You must fill in a title and content"
            t = jinja_env.get_template("newPost.html")
            content = t.render(title=title, body=body, error=error)
            self.response.write(content)
        else:
            blog = Blogs(title=title, body=body)
            blog.put()
            id = blog.key().id()
            self.redirect("/blog/{0}".format(int(id)))

class ViewPostHandler(webapp2.RequestHandler):

    def get(self, id):
        entry = Blogs.get_by_id(int(id))
        t = jinja_env.get_template("entry.html")
        content = t.render(entry = entry)
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPostHandler),
    ('/blog', BlogHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)],
debug=True)


