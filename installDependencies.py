import urllib
print "downloading pip python package manager..."
urllib.urlretrieve ("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
print "downloaded get-pip.py"
print "calling 'python get-pip.py'"
import os

os.system("python get-pip.py")
print "installed pip. Now using it to install dependencies in requirements.txt ..."
os.system("pip install -r requirements.txt")
print "can you see any errors above? if not, you should be good to go. You may need to download Pywin32 manually to distribute this program as exe."


