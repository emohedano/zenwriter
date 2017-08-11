import re
import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from pubsub import pub

from events import EDITOR_TEXT_CHANGED

WPM = 200


class StatusBar(QHBoxLayout):

    def __init__(self):

        self.wrapper = QWidget()

        super(StatusBar, self).__init__(self.wrapper)

        self.wrapper.setStyleSheet('background-color: #FAFAFA')

        self.word_count = 0

        self.wordCountLabel = QLabel()
        self.paragraphCountLabel = QLabel()
        self.readingTimeLabel = QLabel()

        self.addWidget(self.wordCountLabel)
        self.addWidget(self.paragraphCountLabel)
        self.addWidget(self.readingTimeLabel)

        pub.subscribe(self.onEditorTextChanges, EDITOR_TEXT_CHANGED)

    def getWrapper(self):

        return self.wrapper

    def countParagraphs(self, text):

        count = len(text.split('\n\n'))
        label = self.tr('paragraphs')
        self.paragraphCountLabel.setText('{0} {1}'.format(count, label))

    def countWords(self, text):

        self.word_count = len(re.findall(r'\b\w+\b', text))
        return self.word_count

    def displayWordCount(self, text):

        count = self.countWords(text)
        count = "{:,}".format(count)

        label = self.tr('words')
        self.wordCountLabel.setText('{0} {1}'.format(count, label))

    def onEditorTextChanges(self, text):

        self.countParagraphs(text)
        self.displayWordCount(text)
        self.estimateReadingTime()

    def estimateReadingTime(self):

        minutes = math.floor(self.word_count / WPM)

        h, m = divmod(minutes, 60)
        d, h = divmod(h, 24)

        label = self.tr('Estimated reading time')
        self.readingTimeLabel.setText(
            '{0}: {1}d {2}h {3}m'.format(label, d, h, m))
