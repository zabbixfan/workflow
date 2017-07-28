import os,sys

appDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print sys.path.append(appDir)