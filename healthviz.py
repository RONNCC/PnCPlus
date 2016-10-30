
#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import os
from PyQt4 import QtGui
from PyQt4.QtGui import *


def createIntroPage():
    page = QtGui.QWizardPage()
    page.setTitle("Welcome to Healthviz")

    label = QtGui.QLabel("This app will help you import your data and visualize it")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page

def getfile(w,fl):
  fname = QFileDialog.getOpenFileName(w, 'Open file')
  filename = fname
  print fname
  fl.setText(filename)
  #self.le.setPixmap(QPixmap(fname))
    
def choosefile(w,fl):
  fname = QFileDialog.getSaveFileName(w, 'Save file')
  filename = fname
  print fname
  fl.setText(filename)
  #self.le.setPixmap(QPixmap(fname))
 

def createRegistrationPage():
    page = QtGui.QWizardPage()
    page.setTitle("Data Import")
    #page.setSubTitle("Please fill both fields.")

    nameLabel = QtGui.QLabel("CSV File to Import:")
    btn = QPushButton("Select File")
    fileLabel = QtGui.QLabel("")
    btn.clicked.connect(lambda: getfile(page, fileLabel))

    nameLabel2 = QtGui.QLabel("Output File:")
    btn2 = QPushButton("Select File")
    fileLabel2 = QtGui.QLabel("")
    btn2.clicked.connect(lambda: choosefile(page, fileLabel2))



    #emailLabel = QtGui.QLabel("Email address:")
    #emailLineEdit = QtGui.QLineEdit()

    layout = QtGui.QGridLayout()
    layout.addWidget(btn, 0, 0)

    layout.addWidget(nameLabel, 1, 0)
    layout.addWidget(fileLabel, 1, 1)

    layout.addWidget(btn2, 2,0)
    layout.addWidget(nameLabel2, 3, 0)
    layout.addWidget(fileLabel2, 3, 1)

    # layout.addWidget(emailLineEdit, 1, 1)
    page.setLayout(layout)

    return page

def createDataPage():
    page = QtGui.QWizardPage()
    page.setTitle("Data")

    label = QtGui.QLabel("Please see visualizations below")
    label.setWordWrap(True)

    layout = QtGui.QGridLayout()
    layout.addWidget(label,0,0)

    l1 = QtGui.QLabel("-")
    pixmap = QtGui.QPixmap(os.getcwd() + '/cmap2.png')
    print os.getcwd() + '/cmap2.png'
    l1.setPixmap(pixmap)
    layout.addWidget(l1,1,1)


    l2 = QtGui.QLabel("-")
    pixmap = QtGui.QPixmap(os.getcwd() + '/cmap2.png')
    print os.getcwd() + '/cmap1.png'
    l2.setPixmap(pixmap)
    layout.addWidget(l2,1,0)


    page.setLayout(layout)

    return page


def createConclusionPage():
    page = QtGui.QWizardPage()
    page.setTitle("Conclusion")

    label = QtGui.QLabel("You are now done. Have a nice day!")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    wizard = QtGui.QWizard()
    wizard.addPage(createIntroPage())
    wizard.addPage(createRegistrationPage())
    wizard.addPage(createDataPage())
    wizard.addPage(createConclusionPage())

    wizard.setWindowTitle("Trivial Wizard")
    wizard.show()

    sys.exit(wizard.exec_())


"""
import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from PyQt4 import QtGui
 
__author__ = 'pythonspot.com'

# create our window
app = QApplication(sys.argv)
w = QMainWindow()


# Create main menu
mainMenu = w.menuBar()
mainMenu.setNativeMenuBar(False)
fileMenu = mainMenu.addMenu('File')
 
# Add exit button
exitButton = QAction(QIcon('exit24.png'), 'Exit', w)
exitButton.setShortcut('Ctrl+Q')
exitButton.setStatusTip('Exit application')
exitButton.triggered.connect(w.close)
fileMenu.addAction(exitButton)



tabs	= QtGui.QTabWidget()

# Create tabs
tab1	= QtGui.QWidget()	
tab2	= QtGui.QWidget()
tab3	= QtGui.QWidget()
tab4	= QtGui.QWidget()

# Resize width and height
tabs.resize(250, 150)

# Set layout of first tab
vBoxlayout	= QtGui.QVBoxLayout()
pushButton1 = QtGui.QPushButton("Start")
pushButton2 = QtGui.QPushButton("Settings")
pushButton3 = QtGui.QPushButton("Stop")
vBoxlayout.addWidget(pushButton1)
vBoxlayout.addWidget(pushButton2)
vBoxlayout.addWidget(pushButton3)
tab1.setLayout(vBoxlayout)   

# Add tabs
tabs.addTab(tab1,"Tab 1")
tabs.addTab(tab2,"Tab 2")
tabs.addTab(tab3,"Tab 3")
tabs.addTab(tab4,"Tab 4") 

# Set title and show
tabs.setWindowTitle('HealthVizMenu')
tabs.show()


# Show the window and run the app
w.show()
app.exec_()
"""
