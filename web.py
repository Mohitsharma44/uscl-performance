'''
Server to Host WebAPI for USCL-students to 
check the quality of the code they submitted 
for Python Bootcamp @CUSP 2015
'''
__author__ = 'Mohit Sharma'
__version__ = 'Development'

from tornado import gen
import tornado.web
import tornado.ioloop
import motor

class MainHandler(tornado.web.RequestHandler):
        def get(self):
                """Show a 'compose message' form
                """
                self.write('<a href="/check">Check for an entry</a><br>')
                self.write('''
                <form method="post">
                <input type="text" name="msg">
                <input type="submit">
                </form>''')
                            
        # Method exits before the HTTP request completes, thus "asynchronous"
        @tornado.web.asynchronous
        def post(self):
            """Insert a message
            """
            self.write('<a href="/check">Check for an entry</a><br>')
            
            msg = self.get_argument('msg')
            
            # Async insert; callback is executed when insert completes
            self.settings['db'].messages.insert(
                {'msg':msg},
                callback = self._on_response)

        def _on_response(self, result, error):
            if error:
                raise tornado.web.HTTPError(500, error)
            else:
                self.redirect('/')


class MessageHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
                """Display all messages
                """
                self.write('<a href="/new_entry">Compose a message</a><br>')
                self.write('<a href="/check">Check for an entry</a><br>')
                self.write('<ul>')
                db = self.settings['db']
                db.messages.find().sort([('_id', -1)]).each(self._got_message)
                
        def _got_message(self, message, error):
                if error:
                        raise tornado.web.HTTPError(500, error)
                elif message:
                        self.write('<li>%s</li>' % message['msg'])
                else:
                        # Iteration complete
                        self.write('</ul>')
                        self.finish()

class CheckHandler(tornado.web.RequestHandler):
        def get(self):
                '''
                Take input to search
                '''
                self.write('<a href="/new_entry">Compose a message</a><br>')
                self.write('''
                <form method="post">
                <input type='text', name='msg'>
                <input type='submit'>
                </form>
                ''')
                
        @tornado.web.asynchronous
        def post(self):
                '''
                Search for the String
                '''
                self.write('<a href="/new_entry">Compose a message</a><br>')
                self.write('<ul>')
                msg = self.get_argument('msg')
                db = self.settings['db']
                db.messages.find({'msg':msg}).sort([('_id',-1)]).each(self._on_response)
                
        def _on_response(self, message, error):
                if error:
                        raise tornado.web.HTTPError(500, error)
                elif message:
                        self.write('<li>%s</li>'%message['msg'])
                else:
                        #Iteration complete
                        self.write('</ul>')
                        self.finish()

db = motor.MotorClient().test

application = tornado.web.Application([
        (r'/new_entry', MainHandler),
        (r'/', MessageHandler),
        (r'/check', CheckHandler)
], db=db)

def main():
        print 'Listening on 8888'
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
        main()
