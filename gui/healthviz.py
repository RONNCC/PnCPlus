#!/usr/bin/env python

import os, sys, os.path as osp,copy, time
from PyQt4 import QtCore, QtGui
from os.path import isfile, join, basename
import classwizard_rc
from ..scripts.appointment_report_vis import runReport as appointment_report_vis_report
from ..scripts.appointment_util_vis import runReport as appointment_util_vis_report
from ..scripts.ctry_orig import runReport as ctry_orig_report
from ..scripts.total_distinct_patients_vis import runReport as total_distinct_patients_vis_report
from ..scripts.uhs_vis import runReport as uhs_vis_report

FILE_KINDS = ['Appointment Report','Appointment Util','Intl Status/Orig',
             'Total Distinct Patients','UHS Exam Room Vis']

def getReportToCall(reportType):
    if reportType == 'Appointment Report':
        return ('appointment_report_vis.py', appointment_report_vis_report)
    if reportType == 'Appointment Util':
        return ( 'appointment_util_vis.py', appointment_util_vis_report)
    if reportType == 'Intl Status/Orig':
        return ('ctry_orig.py', ctry_orig_report)
    if reportType == 'Total Distinct Patients':
        return ('total_distinct_patients_vis.py', total_distinct_patients_vis_report)
    if reportType == 'UHS Exam Room Vis':
        return ('uhs_vis.py', uhs_vis_report)
    return None, None
    
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

        label = QtGui.QLabel("This app will help you import your data and visualize it<br><br>."+
                             "We will ask for the exported report files you want to visualize "+
                             "and the kind of report file they are!")
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

    def __add_another_row(self,layout):
        k = self.__make_file_choose_row(layout,RegistrationPage.num_in_rows)
        layout.addLayout(k)
        RegistrationPage.num_in_rows+=1

    def __make_file_choose_row(self,layout,rownum):
        thisrownum = copy.copy(rownum)
        btn = QtGui.QPushButton("Select File")
        btn.setToolTip('Select a report file!')
        btn2 = QtGui.QPushButton("+")
        btn2.setToolTip('Add another file')
        fileLabel = QtGui.QLineEdit("")
        fileLabel.setToolTip("The location of the file currently selected")
        btn.clicked.connect(lambda: getfile(self, fileLabel,thisrownum))    
        btn2.clicked.connect(lambda: self.__add_another_row(layout))
        fileKind = QtGui.QComboBox()
        for kind in FILE_KINDS:
            fileKind.addItem(kind)
        fileKind.setToolTip('Choose what kind of report this is - it should be similar to<br>'+
                            'the name of the PointNClick report you used to export the file')
        RegistrationPage.in_files_type[thisrownum] = fileKind.currentText()
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
        tophbox.addWidget(QtGui.QLabel("Choose the report files you would like to use - add more files using the + button"))
        tophbox.addLayout(self.__make_file_choose_row(tophbox,RegistrationPage.num_in_rows))
        RegistrationPage.num_in_rows+=1

        """ BOTTOM HALF """
        nameLabel2 = QtGui.QLabel("&Output Location:")
        DescriptionLabel = QtGui.QLabel("Choose where you want the generated graphs to be saved to")
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
        botvbox.addWidget(DescriptionLabel)
        botvbox.addLayout(outputHbox)

        mainvbox.addLayout(tophbox)
        mainvbox.addStretch(1)
        mainvbox.addLayout(botvbox)

        self.registerField("output_dir*", fileLabel2)
        self.setLayout(mainvbox)


class DataPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(DataPage, self).__init__(parent)
        self.setTitle("Data")
        layout = QtGui.QGridLayout()
        label = QtGui.QLabel("Output should now be generating!")
        loadBar = QtGui.QProgressBar()
        self.loadBar = loadBar
        loadBar.setRange(0,1.0)
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addWidget(loadBar)
        self.setLayout(layout)
        self.doneCreatingGraphs = False

    def createGraphs(self):
        in_files = list(RegistrationPage.in_files.values())
        in_files = [join(in_files, f) for f in in_files if isfile(f)]
        in_files_type = list(RegistrationPage.in_files_type.values())
        in_files_w_type = zip(in_files,in_files_type)
        print 'INFILES /w types: ', in_files_w_type
        print 'OUTPUT DIR:', self.field('output_dir')
        totalToProcess = len(in_files_w_type)*1.0
        doneProcessing = 0
        for file,filetype in in_files_w_type:
            scriptToCall,progToCall = getReportToCall(filetype)
            if scriptToCall == None or progToCall == None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("COULDNT FIND SCRIPT FOR REPORT TYPE: {}".format(filetype))
                msg.setWindowTitle("HEALTHVIZ ERROR")
                
            print '({}/{} RUNNING: '.format(doneProcessing,totalToProcess), scriptToCall, progToCall.__name__
            progToCall(file,self.field('output_dir'))
            doneProcessing += 1
            self.loadBar.setValue(doneProcessing/totalToProcess)
            QtGui.QApplication.processEvents()
        self.doneCreatingGraphs = True  

    def isComplete(self):
        return self.doneCreatingGraphs 

    def initializePage(self):
        time.sleep(0.2)
        self.createGraphs()



def createConclusionPage():
    page = QtGui.QWizardPage()
    page.setTitle("Conclusion")

    label = QtGui.QLabel("You are now done. Have a nice day!")
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page

def runGUI():
    app = QtGui.QApplication(sys.argv)
    wizard = ApplicationWizard() 
    wizard.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    runGUI()
