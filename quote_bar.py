
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

        self.quote_label = QLabel()
        self.author_label = QLabel()

        self.quote_label.setAlignment(Qt.AlignHCenter)
        self.quote_label.setWordWrap(True)
        self.author_label.setAlignment(Qt.AlignRight)

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

        self.addWidget(self.quote_label)
        self.addWidget(self.author_label)

    def getWrapper(self):

        return self.wrapper

    def displayQuote(self):

        self.quote_label.setText('"' + self.quote_text + '"')
        self.author_label.setText('- ' + self.quote_author)