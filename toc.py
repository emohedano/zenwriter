from PyQt5.QtWidgets import QListWidget

class TocView(QListWidget):
    
    def __init__(self):
        super(TocView, self).__init__()

        self.setStyleSheet('QListWidget::item { height: 30; }');