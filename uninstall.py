from subprocess import call
import time
dictionary = {0 : "%s uninstalled sucessfully!"}
print(dictionary[call("pip uninstall PyPDF2")]%"PyPDF2")
print(dictionary[call("pip uninstall appjar")]%"appjar")
print(dictionary[call("pip uninstall pypiwin32")]%"pypiwin32")
print("Required packages uninstalled!")
time.sleep(5)
