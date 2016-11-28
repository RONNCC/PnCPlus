
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

import os, sys, os.path as osp,copy
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
from os.path import isfile, join, basename
import classwizard_rc

FILE_KINDS = ['Appointment Report','Appointment Util','Intl Status/Orig',
             'Total Distinct Patients','UHS Exam Room Vis']

def getReportToCall(reportType):
    if reportType == 'Appointment Report':
        return 'appointment_report_vis.py'
    if reportType == 'Appointment Util':
        return 'appointment_util_vis.py'
    if reportType == 'Intl Status/Orig':
        return 'ctry_orig.py'
    if reportType == 'Total Distinct Patients':
        return 'total_distinct_patients_vis.py'
    if reportType == 'UHS Exam Room Vis':
        return 'uhs_vis.py'
    return None
class ApplicationWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(ApplicationWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(RegistrationPage())
        # self.addPage(PageDataTypesPage())
        self.addPage(DataPage())
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

def getfile(w,fl,rownum):
  fname = QtGui.QFileDialog.getOpenFileName(w, 'Open file')
  filename = fname
  fl.setText(filename)
  RegistrationPage.in_files[rownum]=filename
  #self.le.setPixmap(QPixmap(fname))
    
def choosefile(w,fl):
  fname = QtGui.QFileDialog.getExistingDirectory(w, 'Select Directory')
  fl.setText(fname)

def setReportType(w,fk,thisrownum):
  RegistrationPage.in_files_type[thisrownum] = fk.currentText()

class RegistrationPage(QtGui.QWizardPage):
    num_in_rows=0
    in_files = {}
    in_files_type = {}
    # def in_files_get():
    #     return __input_files

    # def in_files_set(val):
    #     __input_files = val

    # input_files_list = QtCore.pyqtProperty(list, in_files_get, in_files_set)
    def __add_another_row(self,layout):
        k = self.__make_file_choose_row(layout,RegistrationPage.num_in_rows)
        layout.addLayout(k)
        RegistrationPage.num_in_rows+=1

    def __make_file_choose_row(self,layout,rownum):
        thisrownum = copy.copy(rownum)
        btn = QtGui.QPushButton("Select File")
        btn2 = QtGui.QPushButton("+")
        fileLabel = QtGui.QLineEdit("")
        btn.clicked.connect(lambda: getfile(self, fileLabel,thisrownum))    
        btn2.clicked.connect(lambda: self.__add_another_row(layout))
        fileKind = QtGui.QComboBox()
        for kind in FILE_KINDS:
            fileKind.addItem(kind)
        fileKind.currentIndexChanged.connect(lambda: setReportType(self,fileKind,thisrownum))
        selectHBox = QtGui.QHBoxLayout()
        selectHBox.addWidget(btn)
        selectHBox.addWidget(fileLabel)
        selectHBox.addWidget(fileKind)
        selectHBox.addWidget(btn2)
        return selectHBox   

    def __init__(self, parent=None):
        super(RegistrationPage, self).__init__(parent)
        self.registerField("input_files",self,"input_files_list")
        self.setTitle("Data Import")

        #self.setSubTitle("Please fill both fields.")
        tophbox = QtGui.QVBoxLayout()
        botvbox = QtGui.QVBoxLayout()
        mainvbox = QtGui.QVBoxLayout()



        """ TOP DYNAMIC ADD HALF """
        tophbox.addWidget(QtGui.QLabel("CSV Inputs"))
        tophbox.addLayout(self.__make_file_choose_row(tophbox,RegistrationPage.num_in_rows))
        RegistrationPage.num_in_rows+=1

        """ BOTTOM HALF """
        nameLabel2 = QtGui.QLabel("&Output Directory:")
        btn2 = QtGui.QPushButton("Select Directory")
        fileLabel2 = QtGui.QLineEdit("")
        nameLabel2.setBuddy(fileLabel2)
        btn2.clicked.connect(lambda: choosefile(self,fileLabel2))
        outputVbox = QtGui.QVBoxLayout()
        outputVbox.addWidget(nameLabel2)
        outputHbox = QtGui.QHBoxLayout()
        outputHbox.addWidget(btn2)
        outputHbox.addWidget(fileLabel2)
        botvbox.addWidget(nameLabel2)
        botvbox.addLayout(outputHbox)


        mainvbox.addLayout(tophbox)
        mainvbox.addStretch(1)
        mainvbox.addLayout(botvbox)

        # self.registerField("input_dir*", fileLabel)
        self.registerField("output_dir*", fileLabel2)
        # layout.addWidget(emailLineEdit, 1, 1)
        self.setLayout(mainvbox)


class DataPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(DataPage, self).__init__(parent)
        page = QtGui.QWizardPage()
        page.setTitle("Data")
        layout = QtGui.QGridLayout()
        label = QtGui.QLabel("Output should now be generated")
        label.setWordWrap(True)
        layout.addWidget(label)

        page.setLayout(layout)
        return None

    def initializePage(self):
        in_files = list(RegistrationPage.in_files.values())
        in_files = [join(in_files, f) for f in in_files if isfile(f)]
        in_files_type = list(RegistrationPage.in_files_type.values())
        in_files_w_type = zip(in_files,in_files_type)
        for file,filetype in in_files_w_type:
            scriptToCall = getReportToCall(filetype)
            if scriptToCall == None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("COULDNT FIND SCRIPT FOR REPORT TYPE: {}".format(filetype))
                msg.setWindowTitle("HEALTHVIZ ERROR")
            STRING_TO_RUN = "python ../scripts/{} '{}'".format(scriptToCall,file)
            print STRING_TO_RUN
            os.system(STRING_TO_RUN)

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
