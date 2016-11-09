
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

import os, PIL, sys, os.path as osp
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
# import classwizard_rc
from tempfile import NamedTemporaryFile
from os.path import isfile, join, basename
# from PyQt4 import QtGui
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from resizeimage import resizeimage
# # import appointment_report_vis as av
# from PyQt4.QtCore import QObject, pyqtSignal
# from PyQt4 import QtCore, QtGui

import classwizard_rc

FILE_KINDS = ['csv1','csv2','csv3']

class ApplicationWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(ApplicationWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(RegistrationPage())
        self.addPage(PageDataTypesPage())
        self.addPage(createDataPage())
        self.addPage(createConclusionPage())

        self.setPixmap(QtGui.QWizard.BannerPixmap,
                QtGui.QPixmap(':/images/banner.png'))
        self.setPixmap(QtGui.QWizard.BackgroundPixmap,
                QtGui.QPixmap(':/images/background.png'))
        self.setWindowTitle("Healthviz")

class IntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)
        self.setTitle("Welcome to Healthviz")
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                QtGui.QPixmap(':/images/watermark1.png'))

        label = QtGui.QLabel("This app will help you import your data and visualize it")
        label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

def getfile(w,fl):
  fname = QtGui.QFileDialog.getOpenFileName(w, 'Open file')
  filename = fname
  fl.setText(filename)
  #self.le.setPixmap(QPixmap(fname))
    
def choosefile(w,fl):
  fname = QtGui.QFileDialog.getExistingDirectory(w, 'Select Directory')
  fl.setText(fname)

  #self.le.setPixmap(QPixmap(fname))

def output_func_wrapper(w, fl):
    choosefile(w, fl)

class RegistrationPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(RegistrationPage, self).__init__(parent)
        self.setTitle("Data Import")
        #self.setSubTitle("Please fill both fields.")

        nameLabel = QtGui.QLabel("&CSV Input Directory")
        btn = QtGui.QPushButton("Select Directory")
        fileLabel = QtGui.QLineEdit("")
        nameLabel.setBuddy(fileLabel)
        btn.clicked.connect(lambda: choosefile(self, fileLabel))

        nameLabel2 = QtGui.QLabel("&Output Directory:")
        btn2 = QtGui.QPushButton("Select Directory")
        fileLabel2 = QtGui.QLineEdit("")
        nameLabel2.setBuddy(fileLabel2)
        btn2.clicked.connect(lambda: output_func_wrapper(self,fileLabel2))

        #emailLabel = QtGui.QLabel("Email address:")
        #emailLineEdit = QtGui.QLineEdit()

        layout = QtGui.QGridLayout()
        layout.addWidget(btn, 0, 0)

        layout.addWidget(nameLabel, 1, 0)
        layout.addWidget(fileLabel, 1, 1)
        layout.addWidget(QtGui.QLabel(""), 2,0)
        layout.addWidget(QtGui.QLabel(""), 3,0)
        layout.addWidget(btn2, 4,0)
        layout.addWidget(nameLabel2, 5, 0)
        layout.addWidget(fileLabel2, 5, 1)

        self.registerField("input_dir*", fileLabel)
        self.registerField("output_dir*", fileLabel2)
        # layout.addWidget(emailLineEdit, 1, 1)
        self.setLayout(layout)

class PageDataTypesPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(PageDataTypesPage, self).__init__(parent)
        self.setTitle("Types")

        label = QtGui.QLabel("Please choose types below")
        label.setWordWrap(True)

        layout = QtGui.QGridLayout()
        layout.addWidget(label,0,0)

        if self.field('input_dir'):
            print 'yolo', self.field('input_dir')

        self.setLayout(layout)


    def initializePage(self):
        layout = self.layout()
        input_dir = self.field('input_dir')
        print 'CN',input_dir
        outfiles = [join(input_dir, f) for f in os.listdir(input_dir) if isfile(join(input_dir, f))]
        print outfiles
        for ind,item in enumerate(outfiles):
            filenametag = QtGui.QLabel(basename(item))
            fileKind = QtGui.QComboBox()
            for kind in FILE_KINDS:
                fileKind.addItem(kind)
            layout.addWidget(filenametag, ind+1,0)
            layout.addWidget(fileKind,ind+1,1)

def createDataPage():
    page = QtGui.QWizardPage()
    page.setTitle("Data")

    label = QtGui.QLabel("Please see visualizations below")
    label.setWordWrap(True)

    layout = QtGui.QGridLayout()
    layout.addWidget(label,0,0)

    def process_io_directories(io_list):
        print 'IOLIST: ', io_list

    #     # fnmap=[]
    #     # for fn in outfiles:
    #     #     print fn
    #     #     #with open(fn, 'r+b') as f:
    #     #     with PIL.Image.open(fn).load() as image:
    #     #         cover = resizeimage.resize_cover(image, [300, 200])
    #     #         tfn = NamedTemporaryFile()
    #     #         cover.save(tfn.name, image.format)
    #     #         fnmap.append((fn, tfn.name))
    #     # print fnmap

    #     pyfile_location = os.path.dirname(os.path.realpath(__file__))
    #     images_loc= outputdir.text()
    #     print 'IMAGESLOC', images_loc

    outfiles = ['cmap1.jpg','cmap2.png']    
        
    l1 = QtGui.QLabel("-")
    # pixmap = QtGui.QPixmap(fnmap[0][1])
    pixmap = QtGui.QPixmap(outfiles[0])
    l1.setPixmap(pixmap)
    layout.addWidget(l1,1,1)


    l2 = QtGui.QLabel("-")
    # pixmap = QtGui.QPixmap(fnmap[1][1])
    pixmap = QtGui.QPixmap(outfiles[1])
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
    # QtGui.QApplication.setStyle("GTK+")
    wizard = ApplicationWizard() 
    wizard.show()
    sys.exit(app.exec_())


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
