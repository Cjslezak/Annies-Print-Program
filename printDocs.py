#! python3
from appJar import gui
import glob
import win32api
from win32 import win32print
from win32print import *
from win32api import GetSystemMetrics
import win32gui, win32con
import PyPDF2 as pdf

Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)

for x in range(0,10):
    print("SHRINK THIS WINDOW.  DON'T CLOSE IT.  IT'S COMPLETELY IRRELEVANT.")

# top slice - CREATE the GUI
app = gui()

global MainPath
MainPath = None

app.setLocation(0,0)
hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
### fillings go here ###
def Search(btn):
    try:
        for x in optionBoxes:
            app.removeOptionBox(x)
    except:
        pass
    addOptionBoxes()
    currentFolder = []

    for x in optionBoxes:
        for file in glob.glob("J:\\2017 Envelopes\\PDFs\\%s\\*%s*"%(x,app.getEntry('SearchBar'))):
            name = file.rsplit("\\",1)
            currentFolder.append(name[1])
        if currentFolder != []:
            app.changeOptionBox(x,currentFolder,0)
        currentFolder = []
        
    for x in optionBoxes:    
        app.setOptionBoxFunction(x,ChoiceSelect)
        
def none(*args):
    pass

def CreatePdf(path):
    fail = False
    try:
        amount = int(app.getEntry('AmtBar'))
    except ValueError:
        app.retryBox("Error", "Please enter the amount of copies you want.")
        fail = True
    
    if not fail:
        outputFile = open("PrintFile.pdf","wb")
        readDoc = pdf.PdfFileReader(path)
        outDoc = pdf.PdfFileWriter()
        for x in range(0,amount):
            outDoc.appendPagesFromReader(readDoc)
        outDoc.write(outputFile)
        outDoc = None
    return fail
def Print(btn):
    global MainPath
    try:
        if not CreatePdf(MainPath):
            printer = win32print.GetDefaultPrinter()
            printer = win32print.OpenPrinter(printer)

            d = GetPrinter(printer, 2)
            win32api.ShellExecute (0,"print","PrintFile.pdf",'"%s"' %printer,".",0)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            if not app.getCheckBox("Keep print options"):
                try:
                    for x in optionBoxes:
                        app.removeOptionBox(x)
                except:
                    pass
                addOptionBoxes()
                app.setEntryDefault("SearchBar","Search")
                app.setEntryDefault("AmtBar","Amount")
    except:
        app.errorBox("Fatal Error","Please select an item to print")
def ChoiceSelect(box):
    global MainPath
    temp = list(optionBoxes)
    for x in temp:
        if x == box:
            temp.remove(x)
    for x in temp:
        app.disableOptionBox(x)
    MainPath = ("J:\\2017 Envelopes\\PDFs\\%s\\%s"%(box,app.getOptionBox(box)))

for x in range(0,27):\
    app.addLabel("r%s"%x,"",x,0)

def CheckPrinterStatus():
    for x in win32print.EnumPrinters(2):
        print(x[2])

    try:
        printer = win32print.GetDefaultPrinter()
        printer = win32print.OpenPrinter(printer)
        job = EnumJobs(printer, 0 , -1 , 1 )
        print("Pages printed: %s"%job[0]["PagesPrinted"])
    except IndexError:
        pass
app.addEntry("SearchBar",13,0,1)
app.addEntry("AmtBar",13,4,1)

app.addButton("SearchButton",Search,13,1,1)
app.addButton("PrintButton",Print,13,3,1)

app.addCheckBox("Keep print options",12,2)

app.registerEvent(CheckPrinterStatus)

optionBoxes = ["Heirlooms","Organic","Flowers","Bulk small","Bulk large"]

def addOptionBoxes():
    for x in optionBoxes:
        app.addOptionBox(x,["--    %s    --"%x],16,(0+optionBoxes.index(x)),0)  

    app.setOptionBoxFg("Heirlooms","medium blue")
    app.setOptionBoxFg("Organic","olive drab")
    app.setOptionBoxFg("Flowers","deep pink")
    app.setOptionBoxFg("Bulk small","dodger blue")
    app.setOptionBoxFg("Bulk large","dodger blue")

    for x in optionBoxes:   
        app.setOptionBoxAnchor(x,"w")


app.setButton("SearchButton","Search")
app.setButton("PrintButton","Print")
app.setButtonPadding("SearchButton",[0,0])
app.setEntryDefault("SearchBar","Search")
app.setEntryDefault("AmtBar","Amount")

app.setEntryFunction("SearchBar",Search,"<Enter>")
app.setEntryFunction("AmtBar",Print,"<Enter>")
# bottom slice - START the GUI
app.go()

