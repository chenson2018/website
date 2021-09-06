import tornado.template
import mysql.connector
import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        password = os.environ['website_mysql_password']
        username = os.environ['website_mysql_username']
        db = mysql.connector.connect(
          host="localhost",
          user=username,
          password=password,
          database="website"
        )
        
        cursor = db.cursor(dictionary = True)
        cursor.execute("SELECT filename, title, published, publish_date FROM articles ORDER BY publish_date DESC")
        result = cursor.fetchall()

        self.render("index.html", articles = result)

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")

class SubscribeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("subscribe.html", post = False)
    def post(self):
        password = os.environ['website_mysql_password']
        username = os.environ['website_mysql_username']
        db = mysql.connector.connect(
          host="localhost",
          user=username,
          password=password,
          database="website"
        )
        
        email = self.get_body_argument("email", default=None, strip=False)

        cursor = db.cursor(dictionary = True)

        try:
            cursor.execute("INSERT INTO website.emails (email) VALUES (%s);", (email,))
            db.commit()
            self.render("subscribe.html", post = True)
        except:
            raiseError(self, message = "Error subscribing. Most likely your email is already registered, otherwise please contact me.")

class unSubscribeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("unsubscribe.html", post = False)
    def post(self):
        password = os.environ['website_mysql_password']
        username = os.environ['website_mysql_username']
        db = mysql.connector.connect(
          host="localhost",
          user=username,
          password=password,
          database="website"
        )
        
        email = self.get_body_argument("email", default=None, strip=False)

        cursor = db.cursor(dictionary = True)

        try:
            cursor.execute("DELETE FROM website.emails WHERE email = (%s);", (email,))
            db.commit()
            self.render("unsubscribe.html", post = True)
        except:
            raiseError(self, message = "Error unsubscribing, please contact me to resolve.")

class ArticleHandler(tornado.web.RequestHandler):
    def get(self, filename):
        password = os.environ['website_mysql_password']
        username = os.environ['website_mysql_username']

        db = mysql.connector.connect(
          host="localhost",
          user=username,
          password=password,
          database="website"
        )
        
        cursor = db.cursor(dictionary = True)

        cursor.execute("SELECT * FROM articles WHERE filename = %s", (filename,))
        article = cursor.fetchone()

        if article is None:
            self.clear()
            self.set_status(400)
            raiseError(self, message = "Article not found.")
        else:
            filename = os.path.join(os.path.dirname(__file__),
                                    "articles", f"{ article['filename'] }.html")

            with open(filename) as fh:
                body = fh.read()
            self.render("article.html", heading = article['title'], body = body)


def raiseError(self, message):
    self.clear()
    self.set_status(500)
    self.render("error.html", message = message)

if __name__ == "__main__":

    dirname = os.path.dirname(__file__)
    settings = {"template_path": os.path.join(dirname, 'templates'),
                "static_path": "/var/www/chrishenson.net/static/"}

    app =tornado.web.Application([
        (r"/", MainHandler),
        (r"/about", AboutHandler),
        (r"/subscribe", SubscribeHandler),
        (r"/unsubscribe", unSubscribeHandler),
        (r"/article/([a-z_0-9]*)", ArticleHandler),
    ], **settings)
 
    app.listen(int(os.environ['website_port']))
    tornado.ioloop.IOLoop.current().start()
