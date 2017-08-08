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

        self.word_count_label = QLabel()
        self.paragraph_count_label = QLabel()
        self.reading_time_label = QLabel()

        self.addWidget(self.word_count_label)
        self.addWidget(self.paragraph_count_label)
        self.addWidget(self.reading_time_label)   

        pub.subscribe(self.onEditorTextChanges, EDITOR_TEXT_CHANGED)

    def getWrapper(self):

        return self.wrapper

    def countParagraphs(self, text):

        count = len(text.split('\n\n'))
        label = self.tr('paragraphs')
        self.paragraph_count_label.setText('{0} {1}'.format(count, label))

    def countWords(self, text):

        self.word_count = len(re.findall(r'\b\w+\b', text))
        return self.word_count

    def displayWordCount(self, text):

        count = self.countWords(text)
        count = "{:,}".format(count)

        label = self.tr('words')
        self.word_count_label.setText('{0} {1}'.format(count, label))

    def onEditorTextChanges(self, text):
        
        self.countParagraphs(text)
        self.displayWordCount(text)
        self.estimateReadingTime()


    def estimateReadingTime(self):

        minutes = math.floor(self.word_count/WPM)

        h, m = divmod(minutes, 60)
        d, h = divmod(h, 24)

        label = self.tr('Estimated reading time')
        self.reading_time_label.setText('{0}: {1}d {2}h {3}m'.format(label, d, h, m))
        
        
        