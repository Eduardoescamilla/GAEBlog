import os
import webapp2
import jinja2
from google.appengine.ext import db
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Article(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

#Classe base para os outros handlers
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    #Renderiza o html usando o template (Jinja2)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class NewPost(Handler):
	def render_front(self, error = "", subject = "", content = ""):
		self.render("newpost.html", error = error, subject = subject, content = content)
	def get(self):
		self.render_front()
	#Valida a postagem, salva no banco e redireciona para o link definitivo
	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
		if subject and content:
			a = Article(subject = subject, content = content)
			a_key = a.put()

			self.redirect("/%d" %a_key.id())
		else:
			error = "we need both a subject and some content!"
			self.render_front(error, subject, content)
	#Carrega e renderiza um post (link unico)
class PostHandler(Handler):
	def render_front(self, id):
		article = Article.get_by_id(int(id))
		self.render("main.html",  articles = [article])
	def get(self, id):
			self.render_front(id)

	#Carrega e renderiza todos os posts
class MainPage(Handler):
	def render_front(self):
		articles = db.GqlQuery("SELECT * FROM Article ORDER BY created DESC")
		self.render("main.html",  articles = articles)

	def get(self):
		self.render_front()

#Handlers
#O ultimo handler usa expressao regular para acessar o post via o id
app = webapp2.WSGIApplication([('/', MainPage),('/newpost', NewPost), (r'/(\d+)', PostHandler)], debug=True)