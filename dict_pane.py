from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QListWidget, QLineEdit, QListWidgetItem

from mrc_service import MRCService

STYLES ={
    
    "SEARCHBOX" : """
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

        self.words_list = QListWidget()
        self.words_list.setStyleSheet('QListWidget::item { height: 30; }');
        self.words_list.itemPressed.connect(self.onItemPressed)

        definition_wrapper = QWidget()
        definition_layout = QVBoxLayout(definition_wrapper)

        # Avoid weird spacing between layout and it's wrapper
        definition_layout.setSpacing(0)
        definition_layout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.definition_text = QLabel()
        self.definition_text.setOpenExternalLinks(True)
        self.definition_text.setWordWrap(True);

        definition_label = QLabel(self.tr('Definición'))

        definition_layout.addWidget(definition_label)
        definition_layout.addWidget(self.definition_text)

        self.addWidget(self.searchbox, 1)
        self.addWidget(self.words_list, 9)
        self.addWidget(definition_wrapper, 10, Qt.AlignTop)


        data = MRCService.find_synonyms('oscuro')
        self.displaySearchResults(data)

    def getWrapper(self):

        return self.wrapper

    def onReturnPressed(self):
        
        searchword = self.searchbox.text()
        data = MRCService.find_synonyms(searchword)

        self.displaySearchResults(data)


    def displaySearchResults(self, results):

        self.words_list.clear()

        for result in results:

            label = '{0} ({1})'.format(result.word, result.lang)
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, result)

            self.words_list.addItem(item)


    def onItemPressed(self, word):
        
        self.displayWordDetail(word.data(Qt.UserRole))

    def displayWordDetail(self, word):

        gloss = word.gloss;

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

        self.definition_text.setText(label)

