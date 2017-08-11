#!/usr/bin/env python

import signal

from PyQt5.QtCore import QTranslator, QFile, Qt, QTimer, QByteArray, QFileInfo, QMargins, QUrl
from PyQt5.QtGui import QFont, QTextCharFormat, QTextDocumentWriter
from PyQt5.QtWidgets import (QWidget, QApplication, QFileDialog, QMainWindow, QMenu,
        QMessageBox, QSplitter, QVBoxLayout, QTabWidget)
from PyQt5.QtQuick import QQuickView

from pubsub import pub

from editor import ZenTextEdit
from highlighter import Highlighter
from status_bar import StatusBar
from quote_bar import QuoteBar
from toc import TocView
from dict_pane import DictPane

AUTOSAVE_TIMEOUT = 5000

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('Syntax Highlighter')
        self.current_filepath = None

        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupEditor()

        splitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)
        
        toc_pane = TocView()
        quote_bar = QuoteBar()
        status_bar = StatusBar()
        dict_pane = DictPane()


        left_pane_tabs = QTabWidget()
        left_pane_tabs.addTab(toc_pane, 'Índice')
        left_pane_tabs.addTab(QWidget(), 'My Drive')

        center_pane_layout_wrapper = QWidget()
        center_pane_layout = QVBoxLayout(center_pane_layout_wrapper)

        right_pane_tabs = QTabWidget()
        right_pane_tabs.addTab(dict_pane.getWrapper(), 'Diccionario')
        right_pane_tabs.addTab(QWidget(), 'Notas')
        right_pane_tabs.addTab(QWidget(), 'Estadísticas')

        # Avoid weird spacing between layout and it's wrapper
        center_pane_layout.setSpacing(0)
        center_pane_layout.setContentsMargins(QMargins(0, 0, 0, 0))

        center_pane_layout.addWidget(quote_bar.getWrapper())
        center_pane_layout.addWidget(self.editor)
        center_pane_layout.addWidget(status_bar.getWrapper())

        splitter.addWidget(left_pane_tabs)
        splitter.addWidget(center_pane_layout_wrapper)
        splitter.addWidget(right_pane_tabs)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 1)

        self.setCentralWidget(splitter)

        self.openFile('/Users/mohedano/Downloads/30.md')


    def about(self):
        QMessageBox.about(self, 'About ZenWriter',
                '<h1>ZenWriter</h1> by Eduardo Mohedano')

    def setupEditor(self):

        self.editor = ZenTextEdit()
        self.highlighter = Highlighter(self.editor.document())        

    def setupFileMenu(self):
        fileMenu = QMenu(self.tr('File'), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr('New File'), self.newFile, 'Ctrl+N')
        fileMenu.addAction(self.tr('Open...'), self.openFile, 'Ctrl+O')
        fileMenu.addAction(self.tr('Save'), self.saveFile, 'Ctrl+S')
        fileMenu.addAction(self.tr('Save As...'), self.saveFileAs, Qt.CTRL + Qt.SHIFT + Qt.Key_S)
        fileMenu.addAction('Exit', QApplication.instance().quit, 'Ctrl+Q')

    def setupHelpMenu(self):
        helpMenu = QMenu(self.tr('Help'), self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction(self.tr('About'), self.about)


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

        self.setWindowTitle('%s[*]' % (shownName))
        self.setWindowModified(False)

    def openFile(self, path=None):

        if not self.ensureSaved():
            return

        if not path:
            path, _ = QFileDialog.getOpenFileName(self, 'Open File', '',
                'Plain Text Files (*.txt *.md)')

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
        filename, _ = QFileDialog.getSaveFileName(self, 'Save as...', None,
                'Markdown (*.md);; Plain Text (*.txt);;All Files (*)')

        if not filename:
            return False

        filename = filename.lower()
        
        self.setCurrentFileName(filename)
        return self.saveFile()


    def ensureSaved(self):
        
        if not self.editor.document().isModified():
            return True

        ret = QMessageBox.warning(self, 'Application',
                'The document has been modified.\n'
                'Do you want to save your changes?',
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
    

    def closeEvent(self, e):
        if self.ensureSaved():
            e.accept()
        else:
            e.ignore()

if __name__ == '__main__':

    import sys
    
    translator = QTranslator()
    translator.load('translate/es_MX.qm')


    app = QApplication(sys.argv)
    app.installTranslator(translator)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())