
import tempfile
import time
import os
"""
with tempfile.TemporaryDirectory(dir=".") as tmpdirname:
    print('created temporary directory', tmpdirname)
    time.sleep(10)


"""

PATH = tempfile.TemporaryDirectory()

teste = PATH

print(PATH.name)
