import logging
from typing import BinaryIO

import requests
from bs4 import BeautifulSoup

from .exceptions import ProresultException


class WebClient:
    def __init__(self, username, password, dbname):
        self.base_url = "https://proresult.app/adm"
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
        :raises ProresultException: If the login fails.
        :return: The status code of the login request.
        """

        payload = {
            "brnamn": self.username,
            "pass": self.password,
            "dbnamn": self.dbname,
        }

        response = self.session.post(f"{self.base_url}/userlogin.php", data=payload)

        if response.status_code == 200:
            self.logger.debug("Proresult website login successful")
            self.logger.debug(response.text) if self.verbose else None
        else:
            self.logger.error(response.text)
            raise ProresultException(f"Proresult website login failed: {response.text}")

        return response.status_code

    def get_documents(self, folder_id: int):
        """
        Fetches the document metadata from the Proresult website.
        :param folder_id: ID of the folder to look in.
        :return:
        """
        self.logger.debug("Running get_documents...")

        login_website_request = self.session.get(
            f"{self.base_url}/Zdok_get.php?folderId={folder_id}&hideProjectdocs=1"
        )

        login_website = BeautifulSoup(login_website_request.text, "html.parser")

        document_items = login_website.find_all("li", class_="mdl-list__item")

        files_metadata = []

        for item in document_items:
            file_metadata = {}

            # Extract filename
            filename_element = item.find("span", class_="document-name")
            filename_content = (
                filename_element.text.strip() if filename_element else None
            )

            if filename_content is None:
                continue

            file_metadata["FileName"] = str(filename_content)

            # Extract document id
            document_id_element = item.find("div", attrs={"data-document-id": True})
            document_id = (
                document_id_element["data-document-id"] if document_id_element else None
            )

            if document_id is None:
                continue

            file_metadata["Id"] = document_id

            # Extract uploaded date
            uploaded_date_element = item.find("span", class_="document-updated")
            uploaded_date_content = (
                uploaded_date_element.text.strip() if uploaded_date_element else None
            )
            file_metadata["UploadedDate"] = uploaded_date_content

            # add to list
            files_metadata.append(file_metadata)

        self.logger.debug(f"scraped {len(files_metadata)} documents from Proresult")
        self.logger.debug(files_metadata)

        return files_metadata

    def upload_document(self, file_name: str, file_content: BinaryIO, folder_id: int):
        """
        Uploads a document to the ProResult system.
        :param file_name: The name of the file to be uploaded.
        :param file_content: The content of the file to be uploaded.
        :param folder_id: The ID of the folder to upload the file to.
        :return: None
        """
        self.logger.debug(f"Uploading {file_name} to proresult...")
        file = {"document": (file_name, file_content.read())}

        response = self.session.post(
            f"{self.base_url}/Zdok_upload.php?folder={folder_id}", files=file
        )

        if response.status_code != 200:
            raise ProresultException(
                f"Failed to upload {file_name} to proresult: {response.text}"
            )

    def delete_document(self, document_id: int):
        """
        Deletes a document from the ProResult system.
        :param document_id: The ID of the document to be deleted.
        :return: None
        """
        self.logger.debug(f"Deleting document with id {document_id}...")

        response = self.session.get(
            f"{self.base_url}/Zdok.php?action=deleteDocument&dokid={document_id}"
        )

        if response.status_code != 200:
            raise ProresultException(
                f"Error deleting document with id {document_id} from proresult: {response.text}"
            )
