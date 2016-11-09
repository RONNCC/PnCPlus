#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui

import classwizard_rc


class ClassWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        super(ClassWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(ClassInfoPage())

        # self.setPixmap(QtGui.QWizard.BannerPixmap,
        #         QtGui.QPixmap(':/images/banner.png'))
        # self.setPixmap(QtGui.QWizard.BackgroundPixmap,
        #         QtGui.QPixmap(':/images/background.png'))

        self.setWindowTitle("Class Wizard")

    def accept(self):
        className = self.field('className')
        baseClass = self.field('baseClass')
        macroName = self.field('macroName')
        baseInclude = self.field('baseInclude')

        outputDir = self.field('outputDir')
        header = self.field('header')
        implementation = self.field('implementation')

        block = ''

        super(ClassWizard, self).accept()


class IntroPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")
        self.setPixmap(QtGui.QWizard.WatermarkPixmap,
                QtGui.QPixmap(':/images/watermark1.png'))

        label = QtGui.QLabel("This wizard will generate a skeleton C++ class "
                "definition, including a few functions. You simply need to "
                "specify the class name and set a few options to produce a "
                "header file and an implementation file for your new C++ "
                "class.")
        label.setWordWrap(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)



class ClassInfoPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(ClassInfoPage, self).__init__(parent)

        self.setTitle("Class Information")
        self.setSubTitle("Specify basic information about the class for "
                "which you want to generate skeleton source code files.")
        self.setPixmap(QtGui.QWizard.LogoPixmap,
                QtGui.QPixmap(':/images/logo1.png'))

        classNameLabel = QtGui.QLabel("&Class name:")
        classNameLineEdit = QtGui.QLineEdit()
        classNameLabel.setBuddy(classNameLineEdit)

        baseClassLabel = QtGui.QLabel("B&ase class:")
        baseClassLineEdit = QtGui.QLineEdit()
        baseClassLabel.setBuddy(baseClassLineEdit)

        qobjectMacroCheckBox = QtGui.QCheckBox("Generate Q_OBJECT &macro")

        groupBox = QtGui.QGroupBox("C&onstructor")

        qobjectCtorRadioButton = QtGui.QRadioButton("&QObject-style constructor")
        qwidgetCtorRadioButton = QtGui.QRadioButton("Q&Widget-style constructor")
        defaultCtorRadioButton = QtGui.QRadioButton("&Default constructor")
        copyCtorCheckBox = QtGui.QCheckBox("&Generate copy constructor and operator=")

        defaultCtorRadioButton.setChecked(True)

        defaultCtorRadioButton.toggled.connect(copyCtorCheckBox.setEnabled)

        self.registerField('className*', classNameLineEdit)
        self.registerField('baseClass', baseClassLineEdit)
        self.registerField('qobjectMacro', qobjectMacroCheckBox)
        self.registerField('qobjectCtor', qobjectCtorRadioButton)
        self.registerField('qwidgetCtor', qwidgetCtorRadioButton)
        self.registerField('defaultCtor', defaultCtorRadioButton)
        self.registerField('copyCtor', copyCtorCheckBox)

        groupBoxLayout = QtGui.QVBoxLayout()
        groupBoxLayout.addWidget(qobjectCtorRadioButton)
        groupBoxLayout.addWidget(qwidgetCtorRadioButton)
        groupBoxLayout.addWidget(defaultCtorRadioButton)
        groupBoxLayout.addWidget(copyCtorCheckBox)
        groupBox.setLayout(groupBoxLayout)

        layout = QtGui.QGridLayout()
        layout.addWidget(classNameLabel, 0, 0)
        layout.addWidget(classNameLineEdit, 0, 1)
        layout.addWidget(baseClassLabel, 1, 0)
        layout.addWidget(baseClassLineEdit, 1, 1)
        layout.addWidget(qobjectMacroCheckBox, 2, 0, 1, 2)
        layout.addWidget(groupBox, 3, 0, 1, 2)
        self.setLayout(layout)

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = ClassWizard()
    wizard.show()
    sys.exit(app.exec_())
    