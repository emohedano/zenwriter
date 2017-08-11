from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QListWidget, QLineEdit, QListWidgetItem

from mrc_service import MRCService

STYLES = {

    "SEARCHBOX": """
        border-bottom: 2px solid;
        border-color: #CCCCCC;
        padding-bottom: 2;
        padding-top: 2
    """
}


class DictPane(QVBoxLayout):

    def __init__(self):

        self.wrapper = QWidget()

        super(DictPane, self).__init__(self.wrapper)

        self.wrapper.setStyleSheet('background-color: #FFFFFF')

        self.searchbox = QLineEdit()
        self.searchbox.setPlaceholderText('Buscar palabra...')
        self.searchbox.setStyleSheet(STYLES['SEARCHBOX'])
        self.searchbox.setFrame(False)
        self.searchbox.returnPressed.connect(self.onReturnPressed)

        self.wordsList = QListWidget()
        self.wordsList.setStyleSheet('QListWidget::item { height: 30; }')
        self.wordsList.itemPressed.connect(self.onItemPressed)

        definitionWrapper = QWidget()
        definitionLayout = QVBoxLayout(definitionWrapper)

        # Avoid weird spacing between layout and it's wrapper
        definitionLayout.setSpacing(0)
        definitionLayout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.definitionText = QLabel()
        self.definitionText.setOpenExternalLinks(True)
        self.definitionText.setWordWrap(True)

        definitionLabel = QLabel(self.tr('Definición'))

        definitionLayout.addWidget(definitionLabel)
        definitionLayout.addWidget(self.definitionText)

        self.addWidget(self.searchbox, 1)
        self.addWidget(self.wordsList, 9)
        self.addWidget(definitionWrapper, 10, Qt.AlignTop)

        data = MRCService.find_synonyms('oscuro')
        self.displaySearchResults(data)

    def getWrapper(self):

        return self.wrapper

    def onReturnPressed(self):

        searchword = self.searchbox.text()
        data = MRCService.find_synonyms(searchword)

        self.displaySearchResults(data)

    def displaySearchResults(self, results):

        self.wordsList.clear()

        for result in results:

            label = '{0} ({1})'.format(result.word, result.lang)
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, result)

            self.wordsList.addItem(item)

    def onItemPressed(self, word):

        self.displayWordDetail(word.data(Qt.UserRole))

    def displayWordDetail(self, word):

        gloss = word.gloss

        if gloss == 'None':
            gloss = ''
        else:
            gloss += '<br><br>'

        label = """<i>{0}</i> <b>{1}</b> <br><br>
            {2}
            <a href="http://www.wordreference.com/es/en/translation.asp?spen={1}"> Ver en WordReference</a><br>
            <a href="https://es.wikipedia.org/wiki/{1}"> Ver en Wikipedia (español)</a><br>
            <a href="https://en.wikipedia.org/wiki/{1}"> Ver en Wikipedia (inglés)</a>
        """.format(word.type, word.word, gloss)

        self.definitionText.setText(label)
