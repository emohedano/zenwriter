from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextBlockFormat
from PyQt5.QtWidgets import QTextEdit

from pubsub import pub
from utils import throttle

from events import EDITOR_TEXT_CHANGED, TOC_SELECTION_CHANGED

class ZenTextEdit(QTextEdit):

    def __init__(self):

        super(ZenTextEdit, self).__init__()

        font = QFont()
        font.setFamily('Garamond')
        font.setFixedPitch(True)
        font.setPointSize(16)

        self.setAcceptRichText(False)
        self.setFont(font)

        self.setStyleSheet('QTextEdit { background-color: #FFFFFF; border:none; }')

        self.textChanged.connect(self.onTextChanged)
        pub.subscribe(self.onTocSelection, TOC_SELECTION_CHANGED)

    def setPlainText(self, text):
        
        super(ZenTextEdit, self).setPlainText(text)

        #self.justify()
        self.spacify()

    def resizeEvent(self, re):

        self.setViewportMargins(50, 25, 50, 25)
        super(ZenTextEdit, self).resizeEvent(re)

    def justify(self):

        #Make sure the cursor is at the start of the text field
        self.moveCursor(QTextCursor.Start)

        lastPosition = -1
        currPosition = self.textCursor().position()
        
        while lastPosition != currPosition :
            self.setAlignment(Qt.AlignJustify)
            self.moveCursor(QTextCursor.Down)
            lastPosition = currPosition
            currPosition = self.textCursor().position()

        #Move to the end of the text field in preparation for whatever comes next
        self.moveCursor(QTextCursor.End)


    def spacify(self):

        line_height_style = QTextBlockFormat()
        line_height_style.setLineHeight(150, QTextBlockFormat.ProportionalHeight)

        currentBlock = self.document().begin()
        

        while currentBlock.isValid():

            cursor = QTextCursor(currentBlock)
            cursor.setBlockFormat(line_height_style)

            currentBlock = currentBlock.next()


    def onTocSelection(self, item):

        line = item.data(Qt.UserRole)['line']
        
        self.moveCursor(QTextCursor.End)

        cursor = QTextCursor(self.document().findBlockByLineNumber(line))
        self.setTextCursor(cursor)

    @throttle(seconds=1)
    def onTextChanged(self):

        text = self.toPlainText()

        pub.sendMessage(EDITOR_TEXT_CHANGED, text=text)
