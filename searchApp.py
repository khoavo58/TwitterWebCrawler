import tornado.ioloop
import tornado.web
import os.path
from query import search

#get funtion takes in input and post function will display results
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('searchInput.html')

    def post(self):
        q = self.get_body_argument("message")                         #query is a the query string. needs to be parsed and indexed.

        #make the function calls here to get the ranked list. The list must be called results for it to be displayed on the web.

        results = search(q)


        #end of function calls to get ranked list

        self.set_header("Content-Type", "text/plain")
        self.render('listTemplate.html', title = "Results", results = results)  #list variable must be called results

#find files in directories
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    debug=True
)

#this controls what is being ran/displayed for each URL extention
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/results", MainHandler),

    ],**settings)

if __name__ == "__main__":          #loop to web: type "http://localhost:8888" into web browser
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
