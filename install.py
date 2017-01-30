from subprocess import call
import time
dictionary = {0 : "%s installed sucessfully!"}
print(dictionary[call("pip install PyPDF2")]%"PyPDF2")
print(dictionary[call("pip install appjar")]%"appjar")
print(dictionary[call("pip install pypiwin32")]%"pypiwin32")
print("Required packages installed!")
time.sleep(5)
