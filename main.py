#!/usr/bin/env python

import signal, re

from PyQt5.QtCore import QFile, Qt, QTimer, QByteArray, QFileInfo
from PyQt5.QtGui import QFont, QTextCharFormat, QTextDocumentWriter
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
        QMessageBox, QSplitter, QListWidgetItem)

from utils import throttle
from editor import ZenTextEdit
from highlighter import Highlighter
from toc import TocView

AUTOSAVE_TIMEOUT = 5000

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Syntax Highlighter")
        self.current_filepath = None

        splitter = QSplitter()
        self.toc = TocView()

        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupEditor()

        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(self.toc)
        splitter.addWidget(self.editor)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        self.setCentralWidget(splitter)

        self.openFile('/Users/mohedano/Downloads/30.md')


    def about(self):
        QMessageBox.about(self, "About ZenWriter",
                "<h1>ZenWriter</h1> by Eduardo Mohedano")

    def setupEditor(self):

        self.editor = ZenTextEdit()

        self.editor.textChanged.connect(self.onTextEditorChanged)
        self.toc.itemPressed.connect(self.editor.onIndexPressed)

        self.highlighter = Highlighter(self.editor.document())        

    def setupFileMenu(self):
        fileMenu = QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction("&New...", self.newFile, "Ctrl+N")
        fileMenu.addAction("&Open...", self.openFile, "Ctrl+O")
        fileMenu.addAction("&Save...", self.saveFile, "Ctrl+S")
        fileMenu.addAction("Save &As...", self.saveFileAs, Qt.CTRL + Qt.SHIFT + Qt.Key_S)
        fileMenu.addAction("E&xit", QApplication.instance().quit, "Ctrl+Q")

    def setupHelpMenu(self):
        helpMenu = QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction("&About", self.about)


    def newFile(self):

        if not self.ensureSaved():
            return
            
        self.editor.clear()
        self.setCurrentFileName()

    def setCurrentFileName(self, current_filepath=None):
        
        self.current_filepath = current_filepath
        self.editor.document().setModified(False)

        if not self.current_filepath:
            shownName = 'untitled.txt'
        else:
            shownName = QFileInfo(self.current_filepath).fileName()

        self.setWindowTitle(self.tr("%s[*]" % (shownName)))
        self.setWindowModified(False)

    def openFile(self, path=None):

        if not self.ensureSaved():
            return

        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                "Plain Text Files (*.txt *.md)")

        if path:
            inFile = QFile(path)

            if inFile.open(QFile.ReadWrite | QFile.Text):
                
                text = inFile.readAll()
                text = str(text, encoding='utf-8')

                self.editor.setPlainText(text)

        self.setCurrentFileName(path)
        self.initAutoSave()


    def saveFile(self, prompt=True):
        
        if not self.current_filepath:

            if prompt:
                return self.saveFileAs()
            else:
                return
        
        writer = QTextDocumentWriter(self.current_filepath)
        
        ba = QByteArray()
        ba.append('plaintext')

        writer.setFormat(ba)

        text = self.editor.document()
        success = writer.write(text)

        if success:
            self.editor.document().setModified(False)

        return success

    def saveFileAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save as...", None,
                "Markdown (*.md);; Plain Text (*.txt);;All Files (*)")

        if not filename:
            return False

        filename = filename.lower()
        
        self.setCurrentFileName(filename)
        return self.saveFile()


    def ensureSaved(self):
        
        if not self.editor.document().isModified():
            return True

        ret = QMessageBox.warning(self, "Application",
                "The document has been modified.\n"
                "Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.saveFile()

        if ret == QMessageBox.Cancel:
            return False

        return True

    def initAutoSave(self):
        
        self.autosave_timer = QTimer()

        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(AUTOSAVE_TIMEOUT)

    def autosave(self):
    
        self.saveFile(False)

    @throttle(seconds=1)
    def onTextEditorChanged(self):

        text = self.editor.toPlainText()
        lines = text.split('\n')

        self.toc.clear()

        for key, line in enumerate(lines):

            line = line.strip()

            if len(line) > 0 and line[0] == '#':

                element = {
                    'text' : line.replace('#', '    '),
                    'line' : key
                }

                item = QListWidgetItem(element['text'])
                item.setData(Qt.UserRole, element)

                self.toc.addItem(item)


    def closeEvent(self, e):
        if self.ensureSaved():
            e.accept()
        else:
            e.ignore()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())