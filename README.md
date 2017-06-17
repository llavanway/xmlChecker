xmlChecker is a small Python application that performs some checks on credit report xml and produces a note as output. The app is easily adaptable for both Mac and Windows; use the py2app script for Mac and the py2exe script for Windows. Py2exe is not included in the project files but it can be easily found online.

The GUI used is Tkinter. It's old, but fast and it comes with Python.

Two xml checks are performed by the software: the current address on the credit report is compared to an address provided by the user, and the credit report is reviewed for any alerts that contain the words "fraud" or "SSN".

To use, input the credit report in xml form, input the current address you wish to compare to, and click the Check Xml button.

There is also a field that takes as input a "Socure score" if any alerts are found; the produced note will differ depending on whether the Socure score is below or above .3. If no alerts are found, inputting a Socure is unneccesary and will not change the produced note.

Once you've completed your inputs and clicked the Check Xml button, click the Generate Note button. The generated note will automatically be copied to your clipboard, so that you may easily paste it wherever it may be useful.
