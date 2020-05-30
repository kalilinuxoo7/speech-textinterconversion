from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox

"""Global Variables
s2t_t2s(0-s2t, 1-t2s)
mode(0-Online,1-Offline)
input_language(0-English,1-Hindi)
output_languages(0-Excel, 1-text)"""
s2t_t2s = 0
mode = 0
input_language = 0
output_languages = 0


class WindowT2S(QWidget):
    def __init__(self):
        super(WindowT2S, self).__init__()
        self.setWindowTitle("Text to Speech")
        self.resize(640, 480)
        global s2t_t2s, mode, input_language, output_languages
        # create a process output reader
        self.reader = ProcessOutputReader()

        # create a console and connect the process output reader to it
        self.console = MyConsole()
        self.reader.produce_output.connect(self.console.append_output)


        if input_language == 0:
            self.reader.start('python', ['-u', 'textspeech.py'])
            # self.reader.start('./textspeech')
        elif input_language == 1:
            self.reader.start('python', ['-u', 'textspeechhindi.py'])
        else:
            raise ValueError("either English or Hindi is supported")

        # if():
        #     self.reader.start('python', ['-u', 'speech.py'])
        # elif():
        #     self.reader.start('python', ['-u', 'speech.py'])

        self.layout = QVBoxLayout()
        self.label = QLabel("Using Configuration:")
        self.label2 = QLabel("Text to Speech")
        # self.label3 = QLabel("Speech to Text")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label2)
        self.texteditconsole = self.console
        self.layout.addWidget(self.texteditconsole)
        self.setLayout(self.layout)

class WizardT2S(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(WizardT2S, self).__init__(parent)
        self.addPage(Page1t2s(self))
        self.addPage(Page2t2s(self))
        self.setWindowTitle("Text to Speech Configuration Wizard")
        self.resize(640,480)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self._doSomething)


    def _doSomething(self):
        # App = QApplication(sys.argv)
        global mode, input_language, output_languages
        print(mode, input_language, output_languages)
        self.window = WindowT2S()
        self.window.show()
        print('after window show')

class Page1t2s(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1t2s, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Select Language")
        self.layout.addWidget(self.label)

        self.button_eng = QCheckBox("English (default)")
        self.button_eng.setChecked(True)
        self.button_eng.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_eng)

        self.button_hin = QCheckBox("Hindi")
        self.button_hin.setChecked(False)
        self.button_hin.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_hin)

        self.setLayout(self.layout)
        # self.comboBox = QIComboBox(self)
        # self.comboBox.addItem("Python","/path/to/filename1")
        # self.comboBox.addItem("PyQt5","/path/to/filename2")
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.comboBox)
        # self.setLayout(layout)

    @pyqtSlot(int)
    def onStateChange(self, state):
        global input_language
        if state == Qt.Checked:
            if self.sender() == self.button_eng:
                self.button_hin.setChecked(False)
                input_language = 0
            elif self.sender() == self.button_hin:
                self.button_eng.setChecked(False)
                input_language = 1

class Page2t2s(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2t2s, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Save the file to be dictated as text2speech.txt for English \n and text2speechhindi.txt for Hindi and place in the same directory")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)





class QIComboBox(QtWidgets.QComboBox):
    def __init__(self,parent=None):
        super(QIComboBox, self).__init__(parent)




class ProcessOutputReader(QProcess):
    produce_output = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # merge stderr channel into stdout channel
        self.setProcessChannelMode(QProcess.MergedChannels)

        # prepare decoding process' output to Unicode
        codec = QTextCodec.codecForLocale()
        self._decoder_stdout = codec.makeDecoder()
        # only necessary when stderr channel isn't merged into stdout:
        # self._decoder_stderr = codec.makeDecoder()

        self.readyReadStandardOutput.connect(self._ready_read_standard_output)
        # only necessary when stderr channel isn't merged into stdout:
        # self.readyReadStandardError.connect(self._ready_read_standard_error)

    @pyqtSlot()
    def _ready_read_standard_output(self):
        # raw_bytes = self.readAllStandardOutput()
        # text = self._decoder_stdout.toUnicode(raw_bytes)
        raw_bytes = bytearray(self.readAllStandardOutput())
        text = raw_bytes.decode('utf-8')
        self.produce_output.emit(text)

    # only necessary when stderr channel isn't merged into stdout:
    # @pyqtSlot()
    # def _ready_read_standard_error(self):
    #     raw_bytes = self.readAllStandardError()
    #     text = self._decoder_stderr.toUnicode(raw_bytes)
    #     self.produce_output.emit(text)


class MyConsole(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setReadOnly(True)
        self.setMaximumBlockCount(10000)  # limit console to 10000 lines

        self._cursor_output = self.textCursor()
        self.resize(640, 800)

    @pyqtSlot(str)
    def append_output(self, text):
        self._cursor_output.insertText(text)
        self.scroll_to_last_line()

    def scroll_to_last_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else
                            QTextCursor.StartOfLine)
        self.setTextCursor(cursor)

import os
class WindowS2T(QWidget):
    def __init__(self):
        super(WindowS2T, self).__init__()
        self.setWindowTitle("Speech to Text")
        self.resize(640, 480)
        global s2t_t2s, mode, input_language, output_languages
        # create a process output reader
        self.reader = ProcessOutputReader()

        # create a console and connect the process output reader to it
        self.console = MyConsole()
        self.reader.produce_output.connect(self.console.append_output)
        if mode == 0:
            if output_languages == 0:
                if input_language == 0:
                    self.reader.start('python', ['-u', 'speech.py'])

                elif input_language == 1:
                    self.reader.start('python', ['-u', 'speechhindi.py'])
                else:
                    raise ValueError("Not supported")
            elif output_languages == 1:
                if input_language == 0:
                    self.reader.start('python', ['-u', 'speechtext.py'])
                elif input_language == 1:
                    self.reader.start('python', ['-u', 'speechtexthindi.py'])
                else:
                    raise ValueError("Not supported")
        elif mode == 1:
            if output_languages == 0:
                if input_language == 0:
                    # self.reader.start('python', ['-u', 'speechoffline-del.py'])
                    raise ValueError("Medical Application is not supported in offline mode")
                else:
                    raise ValueError("No other language support in offline mode")
            elif output_languages == 1:
                if input_language == 0:
                    self.reader.start('python', ['-u', 'speechtextoffline.py'])
                else:
                    raise ValueError("No other language support in offline mode")
            else:
                raise ValueError("Either Excel or txt is supported")
        else:
            raise ValueError("Mode could be either online or offline")

        # if():
        #     self.reader.start('python', ['-u', 'speech.py'])
        # elif():
        #     self.reader.start('python', ['-u', 'speech.py'])

        self.layout = QVBoxLayout()

        self.label = QLabel("Using Configuration:")
        self.label2 = QLabel("Speech to Text")
        if(mode==0):
            self.label3 = QLabel("Mode : Online")
        else:
            self.label3 = QLabel("Mode : Offline")
        if(input_language==0):
            self.label4 = QLabel("Language : English")
        else:
            self.label4 = QLabel("Language : Hindi")
        if (output_languages == 0):
            self.label5 = QLabel("Application : Excel")
        else:
            self.label5 = QLabel("Application : Simple Text")


        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.label5)

        self.texteditconsole = self.console
        self.layout.addWidget(self.texteditconsole)
        self.setLayout(self.layout)


class NewWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewWizard, self).__init__(parent)
        self.addPage(Pagenewwizard(self))
        self.setWindowTitle("Main Configuration Wizard")
        self.resize(640,480)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self._doSomething)


    def _doSomething(self):
        # App = QApplication(sys.argv)
        # self.window = Window()
        # self.window.show()
        global s2t_t2s
        print(s2t_t2s)
        if(s2t_t2s):
            self.wizardt2s = WizardT2S()
            self.wizardt2s.show()
        else:
            self.magicwizard = MagicWizard()
            self.magicwizard.show()
        # sys.exit(App.exec())
        # msgBox = QtWidgets.QMessageBox()
        # msgBox.setText("Yep, its connected.")
        # msgBox.exec()

class Pagenewwizard(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Pagenewwizard, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Select S2T or T2S")
        self.layout.addWidget(self.label)

        self.button_s2t = QCheckBox("Speech to Text")
        self.button_s2t.setChecked(True)
        self.button_s2t.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_s2t)

        self.button_t2s = QCheckBox("Text to Speech")
        self.button_t2s.setChecked(False)
        self.button_t2s.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_t2s)

        self.setLayout(self.layout)

    @pyqtSlot(int)
    def onStateChange(self, state):
        global s2t_t2s
        if state == Qt.Checked:
            if self.sender() == self.button_t2s:
                self.button_s2t.setChecked(False)
                s2t_t2s = 1
            elif self.sender() == self.button_s2t:
                self.button_t2s.setChecked(False)
                s2t_t2s = 0


class MagicWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.addPage(Page3(self))
        self.setWindowTitle("Speech to text Configuration Wizard")
        self.resize(640,480)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self._doSomething)


    def _doSomething(self):
        # App = QApplication(sys.argv)
        global mode, input_language, output_languages
        print(mode, input_language, output_languages)
        self.window = WindowS2T()
        self.window.show()
        print('after window show')
        # create a process output reader
        # self.reader = ProcessOutputReader()
        #
        # # create a console and connect the process output reader to it
        # self.console = MyConsole()
        # self.reader.produce_output.connect(self.console.append_output)
        #
        # self.reader.start('python', ['-u', 'speech.py'])  # start the process
        # self.console.show()  # make the console visible

        # sys.exit(App.exec())
        # msgBox = QtWidgets.QMessageBox()
        # msgBox.setText("Yep, its connected.")
        # msgBox.exec()

class Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Select Mode")
        self.layout.addWidget(self.label)

        self.button_online = QCheckBox("Online (default)")
        self.button_online.setChecked(True)
        self.button_online.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_online)

        self.button_offline = QCheckBox("Offline(only English is supported)")
        self.button_offline.setChecked(False)
        self.button_offline.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_offline)

        self.setLayout(self.layout)
        # self.comboBox = QIComboBox(self)
        # self.comboBox.addItem("Python","/path/to/filename1")
        # self.comboBox.addItem("PyQt5","/path/to/filename2")
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.comboBox)
        # self.setLayout(layout)

    @pyqtSlot(int)
    def onStateChange(self, state):
        global mode
        if state == Qt.Checked:
            if self.sender() == self.button_offline:
                self.button_online.setChecked(False)
                mode = 1
            elif self.sender() == self.button_online:
                self.button_offline.setChecked(False)
                mode = 0

class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Select Input Language")
        self.layout.addWidget(self.label)
        self.button_english = QCheckBox("English (default)")
        self.button_english.setChecked(True)
        self.button_english.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_english)

        # if(mode==0):
        self.button_hindi = QCheckBox("Hindi")
        self.button_hindi.setChecked(False)
        self.button_hindi.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_hindi)




        self.setLayout(self.layout)

    @pyqtSlot(int)
    def onStateChange(self, state):
        global input_language, mode
        if state == Qt.Checked:
            if self.sender() == self.button_english:
                self.button_hindi.setChecked(False)
                input_language = 0
            elif self.sender() == self.button_hindi:
                # else:
                self.button_english.setChecked(False)
                input_language = 1


class Page3(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Select Application and output type")
        self.layout.addWidget(self.label)
        global mode
        # if (mode == 0):
        #print('online')
        self.button_english = QCheckBox("Medical Application(Output-Excel File) (only in Online Mode)")
        self.button_english.setChecked(True)
        self.button_english.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_english)


        # if (mode == 0):
        #     self.button_hindi.setChecked(False)button_english

        self.button_hindi = QCheckBox("Simple (Output-Text File)")
        self.button_hindi.setChecked(False)
        self.button_hindi.stateChanged.connect(self.onStateChange)
        self.layout.addWidget(self.button_hindi)
        # self.button_both.toggled.connect(
        #     lambda checked: not checked and self.button_hindi.setChecked(True))
        # self.button_both.toggled.connect(
        #     lambda checked: not checked and self.button_english.setChecked(True))

        self.setLayout(self.layout)

    @pyqtSlot(int)
    def onStateChange(self, state):
        global output_languages
        if state == Qt.Checked:
            if (self.sender() == self.button_english):# & (self.sender() !=self.button_both):
                output_languages=0
                self.button_hindi.setChecked(False)
                #self.button_both.setChecked(False)
            if (self.sender() == self.button_hindi):# & (self.sender() !=self.button_both):
                output_languages=1
                self.button_english.setChecked(False)
            # elif (self.sender() == self.button_both):
            #     output_languages = 2
                #self.button_both.setChecked(False)
            #     self.button_english.setChecked(True)
            #     self.button_hindi.setChecked(True)
            # elif self.sender() == self.button_english & self.sender() == self.button_hindi:
            #     self.button_both.setChecked(True)




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # wizard = MagicWizard()
    # wizard.show()
    newwizard = NewWizard()
    newwizard.show()
    sys.exit(app.exec_())