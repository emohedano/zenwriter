from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Zenwriter'

FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'


FILE_FIELDS = 'nextPageToken, files(id, name, parents, mimeType)'
PAGE_SIZE = 100

class FileItem:

    def __init__(self, id, name, mimeType, parents = []):

        self.id = id
        self.name = name
        self.type = 'file'

        if mimeType == FOLDER_MIME_TYPE:
            self.type = 'folder'

        self.mimeType = mimeType
        self.parents = parents
        self.children = []
        

class GoogleDriveServices:

    def __init__(self):
        
        credentials = self.getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v3', http=http)
    
    def getCredentials(self):

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME

            credentials = tools.run_flow(flow, store, flags)

        return credentials

    def fetchFiles(self, q):

        data = []

        results = self.service.files().list(pageSize=PAGE_SIZE, fields=FILE_FIELDS, q=q).execute()
        items = results.get('files', [])
        
        for item in items:

            if 'parents' in item:
                model = FileItem(item['id'], item['name'], item['mimeType'], item['parents'])

                self.fetchChildrenFor(model)

            data.append(model)

        return data

    def fetchRootFiles(self):

        q = 'trashed = false and \'root\' in parents'
        return self.fetchFiles(q)

    def fetchChildrenFor(self, fileModel):

        q = 'trashed = false and \'{}\' in parents'.format(fileModel.id)
        data = self.fetchFiles(q)
        fileModel.children = data
