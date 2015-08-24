import os
from pyunpack import Archive
import subprocess
from patoolib import extract_archive

class UnzipRecursive():
    def __init__(self):
        self.extensions = ('tar.gz', 'zip')
        
    def unzip(self, base_dir):
        for root, dirs, files in os.walk(base_dir):
            if files:
                for i in files:
                    if i.endswith(self.extensions):
                        #print os.path.join(root,i)
                        Archive(os.path.join(root,i)).extractall(os.path.join(root))
                    elif i.endswith('rar'):
                        print i
                        extract_archive(os.path.join(root,i), outdir=os.path.join(root))
if __name__ == '__main__':
    BASE_DIR = '/home/mohitsharma44/assignments/python_core/'
    uz = UnzipRecursive()
    uz.unzip(BASE_DIR)
