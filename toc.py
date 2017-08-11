from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from pubsub import pub

from events import EDITOR_TEXT_CHANGED, TOC_SELECTION_CHANGED


class TocView(QListWidget):

    def __init__(self):
        super(TocView, self).__init__()

        self.setStyleSheet('QListWidget::item { height: 30; }');

        pub.subscribe(self.onEditorTextChanges, EDITOR_TEXT_CHANGED)
        self.itemPressed.connect(self.onItemPressed)

    def onItemPressed(self, item):

        pub.sendMessage(TOC_SELECTION_CHANGED, item=item)

    def onEditorTextChanges(self, text):

        lines = text.split('\n')

        self.clear()

        for key, line in enumerate(lines):

            line = line.strip()

            if len(line) > 0 and line[0] == '#':

                element = {
                    'text': line.replace('#', '    '),
                    'line': key
                }

                item = QListWidgetItem(element['text'])
                item.setData(Qt.UserRole, element)

                self.addItem(item)
