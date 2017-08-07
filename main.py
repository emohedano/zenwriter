#!/usr/bin/env python

import signal, re

from PyQt5.QtCore import QFile, Qt
from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
        QMessageBox, QSplitter, QListWidgetItem)

from utils import throttle
from editor import ZenTextEdit
from highlighter import Highlighter
from toc import TocView


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        splitter = QSplitter()
        self.toc = TocView()

        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupEditor()

        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(self.toc)
        splitter.addWidget(self.editor)

        splitter.setStretchFactor(0, 1);
        splitter.setStretchFactor(1, 2);

        self.setCentralWidget(splitter)
        self.setWindowTitle("Syntax Highlighter")

    def about(self):
        QMessageBox.about(self, "About ZenWriter",
                "<h1>ZenWriter</h1> by Eduardo Mohedano")

    def newFile(self):
        self.editor.clear()

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                    "Plain Text Files (*.txt *.md)")

        if path:
            inFile = QFile(path)

            if inFile.open(QFile.ReadOnly | QFile.Text):
                
                text = inFile.readAll()
                text = str(text, encoding='utf-8')

                self.editor.setPlainText(text)

    def setupEditor(self):

        self.editor = ZenTextEdit()

        self.editor.textChanged.connect(self.onTextEditorChanged)
        self.toc.itemPressed.connect(self.editor.onIndexPressed)

        self.highlighter = Highlighter(self.editor.document())
    
        self.openFile('/Users/mohedano/Downloads/30.md')
        

    def setupFileMenu(self):
        fileMenu = QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction("&New...", self.newFile, "Ctrl+N")
        fileMenu.addAction("&Open...", self.openFile, "Ctrl+O")
        fileMenu.addAction("E&xit", QApplication.instance().quit, "Ctrl+Q")

    def setupHelpMenu(self):
        helpMenu = QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction("&About", self.about)

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

                item = QListWidgetItem(element['text']);
                item.setData(Qt.UserRole, element)

                self.toc.addItem(item)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())