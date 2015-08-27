'''
Server to Host WebAPI for USCL-students to 
check the quality of the code they submitted 
for Python Bootcamp @CUSP 2015
'''
__author__ = 'Mohit Sharma'
__version__ = 'Development'

from tornado import gen
from tornado.options import define, options
import tornado.web
import tornado.ioloop
import motor
import re
import json

# Define default port number if no port number is provided via commandline
define("port", default=8888, help="run on the given port", type=int)

class CheckHandler(tornado.web.RequestHandler):
        '''
        This class provides a web based form to
        search for a string (students name)
        '''
        def get(self):
                '''
                Take input to search
                '''
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
                self.write('<table style="width:50%">')
                username = self.get_argument('username')
                db = self.settings['db']
                self.write('<caption style="text-align:center"><b>%s</b></caption>'%username)
                # Query the Database
                db.performance_collection.find({'name':re.compile(username, re.IGNORECASE)},
                                               {'symbol':1, 'name':1, 'module':1,
                                                'line':1}).sort([{'_id',-1}]).each(self._on_response)

                
        def _on_response(self, message, error):
                '''
                Print the output in tabular format
                '''
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
                        self.finish()

class ApiHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
                '''
                Perform the database querry in get method.
                Accept the string after /api?username= as input
                '''
                a = self.get_argument('username')
                cursor = db.performance_collection.find({'name':re.compile(a, re.IGNORECASE)},
                                               {'_id':0, 'symbol':1, 'name':1, 'module':1,
                                                'line':1}).sort([{'_id',-1}]).each(self._on_response)
                
        def _on_response(self, message, error):
                '''
                Once the request is processed, dump the output 
                in json format and "write" it
                '''
                if error:
                        raise tornado.web.HTTPError(500, error)
                elif message:
                        self.write(json.dumps(message, sort_keys=True, indent=4))
                else:
                        self.finish()

# Database to be used
db = motor.MotorClient().uscl_performance

# Create application
application = tornado.web.Application([
        (r'/check', CheckHandler),
        (r'/api', ApiHandler)
], db=db)

def main():
        # Parse the command line for port number
        tornado.options.parse_command_line()
        print 'Listening on: ',options.port
        application.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
        main()
