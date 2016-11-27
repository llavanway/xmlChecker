from tkinter import *
from tkinter import ttk

root = Tk()
root.title('XmlChecker')

mainFrame = ttk.Frame(root, padding="3 3 12 12")
mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(0, weight=1)

xmlFrame = ttk.LabelFrame(mainFrame, text='Enter xml')
xmlFrame.grid(column=0,row=0)

xmlField = Text(master=xmlFrame, width=35, height=11)
xmlField.pack()

streetNumberFrame = ttk.LabelFrame(mainFrame, text='Enter street number from app')
streetNumberFrame.grid(column=0,row=1)

streetNumberField = ttk.Entry(master=streetNumberFrame)
streetNumberField.pack()

zipCodeFrame = ttk.LabelFrame(mainFrame, text='Enter zip code from app')
zipCodeFrame.grid(column=0,row=2)

zipCodeField = ttk.Entry(master=zipCodeFrame)
zipCodeField.pack()

indicative = 0
current = 0
number = 0
numberEnd = 0
streetNumberXml = 0
streetNumberPass = 0

zip = 0
zipEnd = 0
zipCodeXml = 0
zipCodePass = 0

addressPass = 0

fraudTest1 = 0
fraudTest2 = 0

fraudPass = 0

ssnTest1 = 0
ssnTest2 = 0

ssnPass = 0

note1 = 0
note2 = 0
note3 = 0
note4 = 0

socureScore = 0


def checkXml ():
    """ Perform credit checks in preparation for generateNote. """
    
    global streetNumberPass,zipCodePass,addressPass,fraudPass,ssnPass
    
    resultsField.delete('1.0', END)
    
    xml = xmlField.get('1.0', END).lower() # search terms must be lowercase
    streetNumberApp = streetNumberField.get()
    zipCodeApp = zipCodeField.get()
    
    indicative = xml.find("<indicative>")
    current = xml.find('<status>current</status>',indicative)
    number = xml.find('<number>',current)
    numberEnd = xml.find('</number>',number)
    streetNumberXml = xml[number+8:numberEnd]

    if streetNumberApp == streetNumberXml:
        streetNumberPass = True
    else:
        streetNumberPass = False

    zip = xml.find('<zipcode>',indicative)
    zipEnd = xml.find('</zipcode>',zip)
    zipCodeXml = xml[zip+9:zipEnd]
    
    if zipCodeApp == zipCodeXml:
        zipCodePass = True
    else:
        zipCodePass = False
            
    if streetNumberPass == True and zipCodePass == True:
        addressPass = True
    else:
        addressPass = False


    fraudTest1 = xml.count('fraud')
    fraudTest2 = xml.count('fraud related alert')

    if fraudTest1 == 2 and fraudTest2 == 0:
        fraudPass = True
    else:
        fraudPass = False
    

    ssnTest1 = xml.count('ssn')
    ssnTest2 = xml.count('ssn related alert')
    
    if ssnTest1 == 6 and ssnTest2 == 0:
        ssnPass = True
    else:
        ssnPass = False
    
    
    addressStr1 = 'Address appears to match. Street number from app is '
    addressStr1Fail = 'Address mismatch found. App street number is '
    addressStr2 = ', credit street number is '
    addressStr3 = '. App zip code is '
    addressStr4 = ', credit zip code is '
    addressStr = (addressStr1+str(streetNumberApp)+addressStr2+
    str(streetNumberXml)+addressStr3+str(zipCodeApp)+addressStr4+
    str(zipCodeXml)+'. \n\n')
    addressStrFail = (addressStr1Fail+str(streetNumberApp)+addressStr2+
    str(streetNumberXml)+addressStr3+str(zipCodeApp)+addressStr4+
    str(zipCodeXml)+'. \n\n')
    zipStr = 'No fraud alerts were found. The word fraud appears '
    
    
    if addressPass == True:
        resultsField.insert(END,addressStr)
    else:
        resultsField.insert(END,addressStrFail)
    
    if fraudPass == True:
        resultsField.insert(END,zipStr+str(fraudTest1) + ' times. \n\n')
    else:
        resultsField.insert(END,
        'Fraud alert found. The word fraud appears ' + 
        str(fraudTest1) + ' times. \n\n')
        
    if ssnPass == True:
        resultsField.insert(END,
        'No SSN alerts were found. The word SSN appears ' +
        str(ssnTest1) + ' times.\n\n')
    else:
        resultsField.insert(END,
        'SSN alert found. The word SSN appears ' + 
        str(ssnTest1) + ' times.\n\n')
    
    debugField.delete('1.0',END)
    debugField.insert(END, '\naddressPass = ' + str(addressPass) +
    '\n fraudPass = ' + str(fraudPass) + '\n ssnPass = ' + str(ssnPass))


def generateNote ():
    """ Generates an appropriate ACL note based on check results. """
    
    noteField.delete('1.0', END)    
    
    if fraudPass == False or ssnPass == False:   
        socureScore = float(socureField.get())
    else:
        socureScore = 0
    
    if addressPass == True:
        noteField.insert(END,'Address mismatch CLEAR. \n')
    else:
        noteField.insert(END,
        'Address mismatch FOUND, proof of address required. \n')
    
    if fraudPass == True:
        noteField.insert(END,'Fraud alert CLEAR. \n')
    elif socureScore >= .3:
        noteField.insert(END,
        'Fraud alert FOUND, Socure score is ' + 
        str(socureScore) + '; additional documents required. \n')
    else:
        noteField.insert(END,
        'Fraud alert FOUND, Socure score is ' + 
        str(socureScore) + '. \n' )
        
    if ssnPass == True:
        noteField.insert(END,'SSN alert CLEAR. \n ')
    elif socureScore >= .3:
        noteField.insert(END,
        'SSN alert FOUND, Socure score is ' + 
        str(socureScore) + '; additional documents required. \n')
    else:
        noteField.insert(END,
        'SSN alert FOUND, Socure score is ' + 
        str(socureScore) + '.\n')
        
    root.clipboard_append(noteField.get('1.0', END))
    
    debugField.delete('1.0',END)
    debugField.insert(END, '\naddressPass = ' + str(addressPass) +
    '\n fraudPass = ' + str(fraudPass) + '\n ssnPass = ' + str(ssnPass))
        

b = ttk.Button(mainFrame, text='Check Xml', command=checkXml)
b.grid(column=0,row=3)

resultsFrame = ttk.LabelFrame(mainFrame,text='Results')
resultsFrame.grid(column=0,row=4)

resultsField = Text(master=resultsFrame, width=35, height=11)
resultsField.pack()

socureFrame = ttk.LabelFrame(mainFrame,text='Enter Socure score')
socureFrame.grid(column=0,row=5)

socureField = ttk.Entry(master=socureFrame)
socureField.pack()

b2 = ttk.Button(mainFrame, text='Generate Note', command=generateNote)
b2.grid(column=0,row=6)

noteFrame = ttk.LabelFrame(mainFrame,text='ACL Note')
noteFrame.grid(column=0,row=7)

noteField = Text(master=noteFrame, width=35, height=11)
noteField.pack()

# debug
debugFrame = ttk.LabelFrame(mainFrame,text='Debug')
debugFrame.grid(column=1,row=0)

debugField = Text(debugFrame, width=35, height=11)
debugField.pack()
# /debug

b3 = ttk.Button(mainFrame, text='Quit', command=root.destroy)
b3.grid(column=1,row=2)
    

root.mainloop()

""" TODO:
Format the results messages with line breaks, and add confirmations that 
trigger when fraudTest2 or ssnTest2 fail, to improve user confidence.

Add a generate note button below the results frame that triggers generateNote.

Change the function names to use underscore convention.

Spruce up the interface: add title screen, backgrounds, 
and improve sizing/spacing of widgets.

Package the final program into exe and dmg forms for distribution.

"""
