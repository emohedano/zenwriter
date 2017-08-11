
import urllib.request
import urllib.parse
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget


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

        """
        url = 'http://quotes.rest/qod.json'
        f = urllib.request.urlopen(url)
        body = f.read().decode('utf-8')

        quote = json.loads(body)['contents']['quotes'][0]
        text = quote['quote']
        author = quote['author']
        """

        self.quote_text = 'Estoy convencido de que la autoeducación es el único tipo de educación que existe'
        self.quote_author = 'Isaac Asimov'

        self.displayQuote()

        self.addWidget(self.quoteLabel)
        self.addWidget(self.authorLabel)

    def getWrapper(self):

        return self.wrapper

    def displayQuote(self):

        self.quoteLabel.setText('"' + self.quote_text + '"')
        self.authorLabel.setText('- ' + self.quote_author)
