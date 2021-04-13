import os
import shutil 

for each in os.listdir():
    if os.path.isdir(each):
        try:
            shutil.rmtree(os.path.join(each, '__pycache__'))
        except:
            pass
    try:
        shutil.rmtree('__pycache__')
    except:
        pass