from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextBlockFormat, QCursor
from PyQt5.QtWidgets import QTextEdit

from pubsub import pub
from utils import throttle

from events import EDITOR_TEXT_CHANGED, TOC_SELECTION_CHANGED, EDITOR_REQUEST_FOR_SYNONYM


class ZenTextEdit(QTextEdit):

    def __init__(self):

        super(ZenTextEdit, self).__init__()

        font = QFont()
        font.setFamily('Garamond')
        font.setFixedPitch(True)
        font.setPointSize(16)

        self.setAcceptRichText(False)
        self.setFont(font)

        self.setStyleSheet(
            'QTextEdit { background-color: #FFFFFF; border:none; }')

        self.textChanged.connect(self.onTextChanged)
        pub.subscribe(self.onTocSelection, TOC_SELECTION_CHANGED)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenuEvent)

    def setPlainText(self, text):

        super(ZenTextEdit, self).setPlainText(text)

        # self.justify()
        self.spacify()

    def resizeEvent(self, re):

        self.setViewportMargins(50, 25, 50, 25)
        super(ZenTextEdit, self).resizeEvent(re)

    def justify(self):

        # Make sure the cursor is at the start of the text field
        self.moveCursor(QTextCursor.Start)

        lastPosition = -1
        currPosition = self.textCursor().position()

        while lastPosition != currPosition:
            self.setAlignment(Qt.AlignJustify)
            self.moveCursor(QTextCursor.Down)
            lastPosition = currPosition
            currPosition = self.textCursor().position()

        # Move to the end of the text field in preparation for whatever comes
        # next
        self.moveCursor(QTextCursor.End)

    def spacify(self):

        lineHeightStyle = QTextBlockFormat()
        lineHeightStyle.setLineHeight(
            150, QTextBlockFormat.ProportionalHeight)

        currentBlock = self.document().begin()

        while currentBlock.isValid():

            cursor = QTextCursor(currentBlock)
            cursor.setBlockFormat(lineHeightStyle)

            currentBlock = currentBlock.next()

    def onTocSelection(self, item):

        line = item.data(Qt.UserRole)['line']

        self.moveCursor(QTextCursor.End)

        cursor = QTextCursor(self.document().findBlockByLineNumber(line))
        self.setTextCursor(cursor)

    def onContextMenuEvent(self, pos):

        selectedWord = self.textCursor().selectedText()
        menu = self.createStandardContextMenu(pos)
        menuItem = menu.addAction('Buscar sinónimos para "{0}"'.format(selectedWord))
        menuItem.triggered.connect(self.onSynonymLookup)
        menu.exec_(self.viewport().mapToGlobal(pos))

    def onSynonymLookup(self, e):
        
        selectedWord = self.textCursor().selectedText()
        pub.sendMessage(EDITOR_REQUEST_FOR_SYNONYM, word=selectedWord)

    @throttle(seconds=1)
    def onTextChanged(self):

        text = self.toPlainText()

        pub.sendMessage(EDITOR_TEXT_CHANGED, text=text)
