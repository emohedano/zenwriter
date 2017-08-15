import re
import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from pubsub import pub
from langdetect import detect

from utils.events import EDITOR_TEXT_CHANGED

WPM = 200


class StatusBar(QHBoxLayout):

    def __init__(self):

        self.wrapper = QWidget()

        super(StatusBar, self).__init__(self.wrapper)

        self.wrapper.setStyleSheet('background-color: #FAFAFA')

        self.wordCount = 0
        self.currentLang = 'N/A'

        self.wordCountLabel = QLabel()
        self.langLabel = QLabel()
        self.readingTimeLabel = QLabel()

        self.addWidget(self.langLabel)
        self.addWidget(self.wordCountLabel)
        self.addWidget(self.readingTimeLabel)

        pub.subscribe(self.onEditorTextChanges, EDITOR_TEXT_CHANGED)

    def getWrapper(self):

        return self.wrapper

    def countWords(self, text):

        self.wordCount = len(re.findall(r'\b\w+\b', text))
        return self.wordCount

    def displayWordCount(self, text):

        count = self.countWords(text)
        count = "{:,}".format(count)

        label = self.tr('words')
        self.wordCountLabel.setText('{0} {1}'.format(count, label))

    def onEditorTextChanges(self, text):

        self.displayWordCount(text)
        self.estimateReadingTime()
        self.detectLang(text)

    def estimateReadingTime(self):

        minutes = math.floor(self.wordCount / WPM)

        h, m = divmod(minutes, 60)
        d, h = divmod(h, 24)

        label = self.tr('Estimated reading time')
        self.readingTimeLabel.setText(
            '{0}: {1}d {2}h {3}m'.format(label, d, h, m))

    def detectLang(self, text):

        try:
            
            abstract = text[:1000]
            self.currentLang = detect(abstract)

            self.currentLang = self.currentLang.upper()

            label = self.tr('Language')
            self.langLabel.setText('{0}: {1}'.format(label, self.currentLang))

        except Exception as e:
            pass
