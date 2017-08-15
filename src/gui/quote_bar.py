
import urllib.request
import urllib.parse
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget

from services.quotes_service import QuotesService

class QuoteBar(QVBoxLayout):

    def __init__(self):

        self.wrapper = QWidget()

        super(QuoteBar, self).__init__(self.wrapper)

        self.wrapper.setStyleSheet('background-color: #FAFAFA')

        self.quoteLabel = QLabel()
        self.authorLabel = QLabel()

        self.quoteLabel.setAlignment(Qt.AlignHCenter)
        self.quoteLabel.setWordWrap(True)
        self.authorLabel.setAlignment(Qt.AlignRight)

        self.quote = QuotesService.getRandomQuote()

        self.displayQuote()

        self.addWidget(self.quoteLabel)
        self.addWidget(self.authorLabel)

    def getWrapper(self):

        return self.wrapper

    def displayQuote(self):

        self.quoteLabel.setText('"' + self.quote.text + '"')
        self.authorLabel.setText('- ' + self.quote.author)
