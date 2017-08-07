from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat

import pmh4python

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):

        super(Highlighter, self).__init__(parent)

        self.highlightingRules = {}

        H1 = QTextCharFormat()
        H1.setFontPointSize(30)

        H2 = QTextCharFormat()
        H2.setFontPointSize(24)

        H3 = QTextCharFormat()
        H3.setFontPointSize(20)

        H4 = QTextCharFormat()
        H4.setFontPointSize(18)

        STRONG = QTextCharFormat()
        STRONG.setFontWeight(QFont.Bold)

        EMPH = QTextCharFormat()
        EMPH.setFontItalic(True)

        self.highlightingRules['H1'] = H1
        self.highlightingRules['H2'] = H2
        self.highlightingRules['H3'] = H3
        self.highlightingRules['H4'] = H4
        self.highlightingRules['STRONG'] = STRONG
        self.highlightingRules['EMPH'] = EMPH


    def highlightBlock(self, text):

        results = pmh4python.parse_markdown(text)

        for element_type, elements in results.items():

            if element_type in self.highlightingRules:

                element_styles = self.highlightingRules[element_type]

                for element in elements:

                    index = element['start']
                    length = element['end'] - index

                    self.setFormat(index, length, element_styles)


        self.setCurrentBlockState(0)