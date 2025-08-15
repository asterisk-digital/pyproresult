import csv
import logging

import requests
import lxml.etree as et


class CsvDataError(Exception):
    pass


class ApiClient:
    def __init__(self, api_url: str, account_id: str, api_secret: str):
        self.api_url = f'https://{api_url}/soap/tmcapi.php'
        self.account_id = account_id
        self.api_secret = api_secret
        self.headers = {
            'X-Account-ID': self.account_id,
            'X-API-Secret': self.api_secret,
        }

    def get_csv_data(self, function: str):
        """
        Gets data from Proresult as CSV
        :param function: The function to call in tmcapi.php
        :raises CsvDataError: If the data is not available or the request fails
        :return:
        """
        url = self.api_url + '?fn=' + function

        response = requests.get(url, headers=self.headers, timeout=60)

        if response.status_code >= 300:
            raise CsvDataError(
                f'Error getting CSV data, bad status code: {response.status_code} {response.text}')

        # Doesn't pass encoding header correctly, but it's utf-8
        csv_data_raw = response.content.decode('utf-8')

        # Alternate error condition, they still send us 200 OK so we need to check the body
        if 'TMCAPI - ingen tilgang' in csv_data_raw:
            raise CsvDataError(
                'Error getting CSV data, no access: ' + response.text)

        # Parse csv data
        csv_reader = csv.DictReader(csv_data_raw.splitlines(), delimiter=';')
        csv_data = list(csv_reader)

        return csv_data

    def get_deviations(self):
        """
        :return: List of deviations with ids, names etc.
        """
        csv_data = self.get_csv_data('hse_deviationCSV')
        return csv_data

    def get_workers(self):
        """
        :return: List of workers with names, ids etc.
        """
        workers = self.get_csv_data('tilsettCSV')
        return workers

    def get_images(self, deviation_id: int) -> {}:
        """
        :param deviation_id: The id of the deviation to get images for
        :return: Dict with filename as key and url as value
        """
        url = self.api_url + f"?fn=hentBilder&hse_deviationId={deviation_id}"
        response = requests.get(url, headers=self.headers, timeout=60)

        if response.status_code >= 300:
            raise Exception(
                f'Error getting images, bad status code: {response.status_code} {response.text}')

        # Doesn't pass encoding header correctly, but it's utf-8
        xml_data_raw = response.content.decode('utf-8')

        # Alternate error condition, they still send us 200 OK so we need to check the body
        if 'TMCAPI - ingen tilgang' in xml_data_raw:
            raise Exception(
                f'Error getting image XML data, no access: {response.text}')

        images = {}

        # Parse xml data (fromstring takes a, uh, bytes-like object and not a string)
        root = et.fromstring(response.content)
        xml_images = root.xpath('/Bilder/Bilde')

        for image in xml_images:
            url = image.find("Url").text
            filename = image.find("Filnavn").text

            if filename in images:
                logging.warning(f'In PR deviation {deviation_id} image {filename} is duplicate, skipping')
                continue

            images[filename] = url

        return images
