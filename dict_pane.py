from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QListWidget, QLineEdit, QListWidgetItem

from pubsub import pub

from mrc_service import MRCService
from events import EDITOR_REQUEST_FOR_SYNONYM

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

        self.wrapper.setStyleSheet('background-color: #FFFFFF; QListWidget{ border: none; }')

        self.searchbox = QLineEdit()
        self.searchbox.setPlaceholderText('Buscar palabra...')
        self.searchbox.setStyleSheet(STYLES['SEARCHBOX'])
        self.searchbox.setFrame(False)
        self.searchbox.returnPressed.connect(self.onReturnPressed)

        self.wordsList = QListWidget()
        self.wordsList.setStyleSheet('QListWidget::item { height: 30; }')
        self.wordsList.currentItemChanged.connect(self.onSelectionChanged)

        definitionWrapper = QWidget()
        definitionLayout = QVBoxLayout(definitionWrapper)

        # Avoid weird spacing between layout and it's wrapper
        definitionLayout.setSpacing(0)
        definitionLayout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.definitionText = QLabel()
        self.definitionText.setWordWrap(True)
        self.definitionText.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        self.definitionText.setOpenExternalLinks(True)


        definitionLabel = QLabel(self.tr('Definición'))

        definitionLayout.addWidget(definitionLabel)
        definitionLayout.addWidget(self.definitionText)

        self.addWidget(self.searchbox, 1)
        self.addWidget(self.wordsList, 9)
        self.addWidget(definitionWrapper, 10, Qt.AlignTop)

        data = MRCService.find_synonyms('oscuro')
        self.displaySearchResults(data)

        pub.subscribe(self.lookUpDefinitions, EDITOR_REQUEST_FOR_SYNONYM)

    def getWrapper(self):

        return self.wrapper

    def onReturnPressed(self):

        searchword = self.searchbox.text()
        self.lookUpDefinitions(searchword)

    def lookUpDefinitions(self, word):

        self.searchbox.setText(word)
        data = MRCService.find_synonyms(word)

        if not data:
            self.displayEmptySearchResults(word)
        else:
            self.displaySearchResults(data)

    def displaySearchResults(self, results):

        self.wordsList.clear()

        for result in results:

            label = '{0} {1}_{2}'.format(result.type, result.word, result.sense)

            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, result)

            self.wordsList.addItem(item)

    def displayEmptySearchResults(self, word):

        self.wordsList.clear()
        self.wordsList.addItem('No se encontraron coincidencias')

        label = """<b>{0}</b> <br><br>
            <a href="http://www.wordreference.com/es/en/translation.asp?spen={0}"> WordReference</a><br>
            <a href="https://es.wikipedia.org/wiki/{0}"> Wikipedia (español)</a><br>
            <a href="https://en.wikipedia.org/wiki/{0}"> Wikipedia (inglés)</a>
        """.format(word)

        self.definitionText.setText(label)

    def onSelectionChanged(self, currentItem, previousItem):

        if not currentItem:
            return

        mrcWord = currentItem.data(Qt.UserRole)
        self.displayWordDetail(mrcWord)

    def displayWordDetail(self, mrcWord):

        if not mrcWord:
            return

        gloss = mrcWord.gloss
        examples = ''
        synonyms = ''

        if gloss == 'None':
            gloss = ''
        else:
            gloss += '<br><br>'

        if mrcWord.synonyms:
            synonyms = (', ').join(mrcWord.synonyms)
            synonyms = 'Sinónimos: <i>' + synonyms + '</i><br><br>'

        if mrcWord.examples:
            examples = ('<br>').join(mrcWord.examples)
            examples = 'Ejemplos:<br><br><i>' + examples + '</i>'

        label = """<i>{0}</i> <b>{1}_{5}</b> <br><br>
            {2}{3}{4}
            <a href="http://www.wordreference.com/es/en/translation.asp?spen={1}"> WordReference</a>, 
            <a href="https://es.wikipedia.org/wiki/{1}"> Wikipedia </a>
        """.format(mrcWord.type, mrcWord.word, gloss, synonyms, examples, mrcWord.sense)

        self.definitionText.setText(label)