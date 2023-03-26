
import os, fnmatch

dir = '/home/cr625/webads/html/'
files = fnmatch.filter(os.listdir(dir), '*.html')
print(files)