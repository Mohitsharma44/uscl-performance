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
import re
import json

class CheckHandler(tornado.web.RequestHandler):

        def access_db(self):
                print 'Accessing db'
        
        def get(self):
                '''
                Take input to search
                '''
                self.write('<a href="/new_entry">Compose a message</a><br>')
                self.write('''
                <form method="post">
                <input type='text', name='username'>
                <input type='submit'>
                </form>
                ''')
                
        @tornado.web.asynchronous
        def post(self):
                '''
                Search for the String
                '''
                self.write('<a href="/new_entry">Compose a message</a><br>')
                self.write('<table style="width:50%">')
                username = self.get_argument('username')
                db = self.settings['db']
                self.write('<caption style="text-align:center"><b>%s</b></caption>'%username)
                db.performance_collection.find({'name':re.compile(username, re.IGNORECASE)},
                                               {'symbol':1, 'name':1, 'module':1,
                                                'line':1}).sort([{'_id',-1}]).each(self._on_response)

                #db.performance_collection.find({'name':re.compile(username, re.IGNORECASE)}).count()
                
        def _on_response(self, message, error):
                try:
                        self.count = len(message['module'])
                except Exception, e:
                        pass
                if error:
                        raise tornado.web.HTTPError(500, error)
                elif message:
                        self.write('<tr>')
                        self.write('<th style="text-align:left"> Message </th>')
                        self.write('<th style="text-align:left"> Program Name (.py) </th>')
                        self.write('<th style="text-align:left"> Line no. </th>')
                        for i in range(len(message['symbol'])):
                                self.write('<tr>')
                                self.write('<td>%s</td><td>%s</td><td>%s</td>'%(message['symbol'][i],
                                                                                message['module'][i],
                                                                                message['line'][i]))
                                self.write('</tr>')
                else:
                        #Iteration complete
                        self.write('</table><br><br>')
                        #self.write('<b>Total Submissions Done: %d</b>'%self.count)
                        self.finish()

class ApiHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
                a = self.get_argument('username')
                cursor = db.performance_collection.find({'name':re.compile(a, re.IGNORECASE)},
                                               {'_id':0, 'symbol':1, 'name':1, 'module':1,
                                                'line':1}).sort([{'_id',-1}]).each(self._on_response)
        def _on_response(self, message, error):
                if error:
                        raise tornado.web.HTTPError(500, error)
                elif message:
                        self.write(json.dumps(message, sort_keys=True, indent=4))
                else:
                        self.finish()
                        
        @tornado.web.asynchronous
        def post(self):
                pass

                        
db = motor.MotorClient().uscl_performance

application = tornado.web.Application([
        (r'/check', CheckHandler),
        (r'/api', ApiHandler)
], db=db)

def main():
        print 'Listening on 8888'
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
        main()
