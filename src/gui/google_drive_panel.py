from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
from PyQt5.QtWidgets import QTreeView, QAbstractItemView

from pubsub import pub

from services.google_drive_service import GoogleDriveServices

FILE_ICON = QIcon('controls/file.svg')
TEXTFILE_ICON = QIcon('controls/file-document.svg')
FOLDER_ICON = QIcon('controls/folder.svg')
IMAGE_ICON = QIcon('controls/file-image.svg')

class GoogleDriveExplorerView(QTreeView):

    def __init__(self):
        super(GoogleDriveExplorerView, self).__init__()

        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([self.tr('Archivo')])

        self.setModel(self.model)
        self.setUniformRowHeights(True)

        self.driveServices = GoogleDriveServices()
        self.renderFileTree()

    def renderFileTree(self):

        data = self.driveServices.fetchRootFiles()

        for element in data:
            self.renderFileTreeLevel(element, self.model)

    def renderFileTreeLevel(self, _element, parent=False):

        treeItem = QStandardItem(_element.name)
        fileIcon = FILE_ICON

        if _element.type == 'folder':
            fileIcon = FOLDER_ICON
        elif _element.mimeType.startswith('image/'):
            fileIcon = IMAGE_ICON
        elif _element.mimeType.startswith('text/'):
            fileIcon = TEXTFILE_ICON

        treeItem.setIcon(fileIcon)
        treeItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

        parent.appendRow([treeItem])

        for element in _element.children:
            self.renderFileTreeLevel(element, treeItem)
