import json
import pymongo
import subprocess
import os
from collections import defaultdict
#from pyprind import ProgBar

class CodeTester():
    '''
    Class to scan a directory for py files recursively,
    Perform Quality of Code checks using pylint
    
    '''
    def __init__(self):
        self.users = []
        self.files = []

    def get_py_files(self, base_dir):
        '''
        Scan for py files recursively.
        Arguments required: base_dir <str>
        '''
        for root, dirs, files in os.walk(base_dir):
            if files:
                for i in files:
                    if i.endswith('py'):
                        self.users.append(root.split('/')[5])
                        self.files.append(os.path.join(root, i))

        return self.files, self.users
    
    def check_code(self, fpath):
        '''
        Scan for the quality of code using pylint
        Arguments required: fpath <str>
        '''
        # Use custom pylintrc file and call pylint
        pout = subprocess.Popen(['pylint', fpath,
                              '--rcfile=pylintrc.txt','-f',
                              'json'], stdout=subprocess.PIPE).stdout.read()

        return pout

    def parse_for_db(self, li, username):
        '''
        Parse the list (output of check_codes) and 
        username to JSON to be able to add to DB.
        Arguments required: li <list>, username <str>
        '''
        try:
            self.dict_formatted_li = defaultdict(list)
            self.json_formatted_li = json.loads(li)
        except Exception, err:
            # Errors that rises because people have copy pasted ipython interpreter.
            print 'Copy Pasted ipython interpreter? ',err
            pass
            
        # Add list of dictionaries to defaultdict (of type list)
        for i in self.json_formatted_li:
            for key, value in i.iteritems():
                self.dict_formatted_li[key].append(value)
                
        # Add username to the dictionary        
        self.dict_formatted_li['name'] = ''.join(username.split('_'))
        # Convert to json format
        self.json_formatted_di = json.dumps(self.dict_formatted_li, sort_keys=True, indent=4)
        
        return self.json_formatted_di

    def add_to_db(self, di):
        '''
        Add the dictionary (output of parse_for_db) to DB
        Arguments required: di <dict>
        '''
        json_formatted_di = json.loads(di)
        # Connecting to pymongo server
        conn = pymongo.MongoClient()
        # Using database
        db = conn.uscl_performance
        # using testcollection
        collection = db.performance_collection
        # Inserting data
        collection.insert(json_formatted_di)

        return collection.find().sort([{'_id',-1}]).limit(1)
    
if __name__ == '__main__':
    BASE_DIR = '/home/mohitsharma44/assignments/python_core'
    
    ct = CodeTester()
    test = []
    i = 0
    files, users = ct.get_py_files(BASE_DIR)

    #proc_bar = ProgBar(len(files), bar_char='#', monitor=True, title='Code Checking Operation')
    
    for f in files:
        print 'Scanning: ',users[i]
        test.append(ct.check_code(f))
        i +=1
        #proc_bar.update()
    #print proc_bar

    #db_bar = ProgBar(len(test), bar_char='#', monitor=True, title='Database Operation')
        
    for i in range(len(test)):
        print 'Adding ',users[i], '\'s submission to database'
        d = ct.parse_for_db(test[i], users[i])
        print 'Collection Updated: ',ct.add_to_db(d)
        #db_bar.update()
    #print db_bar
