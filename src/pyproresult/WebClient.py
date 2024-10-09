import logging

import requests
from bs4 import BeautifulSoup


class WebClient:
    def __init__(self, base_url, username, password, dbname):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.dbname = dbname
        self.session = requests.Session()
        self.verbose = False
        self.logger = logging.getLogger(__name__)

        self.login()

    def login(self):
        """
        Logs in to the Proresult website using the provided payload.
        :raises Exception: If the login fails.
        :return: The status code of the login request.
        """

        payload = {
            'brnamn': self.username,
            'pass': self.password,
            'dbnamn': self.dbname
        }

        response = self.session.post(f'{self.base_url}/userlogin.php', data=payload)

        if response.status_code == 200:
            logging.debug(f'Proresult website login successful')
            logging.debug(response.text) if self.verbose else None
        else:
            logging.error(response.text)
            raise Exception(f'Proresult website login failed: {response.text}')

        return response.status_code

    def get_documents(self, folder_id: int):
        """
        Fetches the document metadata from the Proresult website.
        :param folder_id: ID of the folder to look in.
        :return:
        """
        self.logger.debug('Running get_documents...')

        login_website_request = self.session.get(
            f'{self.base_url}/Zdok_get.php?folderId={folder_id}&hideProjectdocs=1')

        login_website = BeautifulSoup(login_website_request.text, 'html.parser')

        document_items = login_website.find_all('li', class_='mdl-list__item')

        files_metadata = []

        for item in document_items:
            file_metadata = {}

            # Extract filename
            filename_element = item.find('span', class_='document-name')
            filename_content = filename_element.text.strip() if filename_element else None

            if filename_content is None:
                continue

            filename = str(filename_content).replace('.pdf', '')
            file_metadata['FileName'] = filename

            # Extract document id
            document_id_element = item.find('div', attrs={'data-document-id': True})
            document_id = document_id_element['data-document-id'] if document_id_element else None

            if document_id is None:
                continue

            file_metadata['Id'] = document_id

            # Extract uploaded date
            uploaded_date_element = item.find('span', class_='document-updated')
            uploaded_date_content = uploaded_date_element.text.strip() if uploaded_date_element else None
            file_metadata['UploadedDate'] = uploaded_date_content

            # add to list
            files_metadata.append(file_metadata)

        logging.debug(f'scraped {len(files_metadata)} documents from Proresult')
        logging.debug(files_metadata)

        return files_metadata
