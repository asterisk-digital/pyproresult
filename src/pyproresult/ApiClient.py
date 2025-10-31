import csv
import logging

import requests
import lxml.etree as et


class CsvDataError(Exception):
    pass


class ApiClient:
    def __init__(self, account_id: str, api_secret: str):
        self.api_url = f"https://proresult.app/soap/tmcapi.php"
        self.account_id = account_id
        self.api_secret = api_secret
        self.headers = {
            "X-Account-ID": self.account_id,
            "X-API-Secret": self.api_secret,
        }

    def get_csv_data(self, function: str, query_params: dict | None = None) -> list[dict]:
        """
        Gets data from Proresult as CSV
        :param function: The function to call in tmcapi.php
        :param query_params: Optional query parameters to pass to the API
        :raises CsvDataError: If the data is not available or the request fails
        :return:
        """
        url = self.api_url + "?fn=" + function
        if query_params:
            parts = [f"{key}={value}" if value is not None else f"{key}" for key, value in query_params.items()]
            url += "&" + "&".join(parts)

        response = requests.get(url, headers=self.headers, timeout=60)

        if response.status_code >= 300:
            raise CsvDataError(f"Error getting CSV data, bad status code: {response.status_code} {response.text}")

        # The response from the API doesn't pass encoding header correctly, but we know it's utf-8
        csv_data_raw = response.content.decode("utf-8")

        # Alternate error condition, they still send us 200 OK so we need to check the body
        if "TMCAPI - ingen tilgang" in csv_data_raw:
            raise CsvDataError("Error getting CSV data, no access: " + response.text)

        # Parse csv data
        csv_reader = csv.DictReader(csv_data_raw.splitlines(), delimiter=";")
        csv_data = list(csv_reader)

        return csv_data

    def get_deviations(self) -> list[dict]:
        """
        :return: List of deviations with ids, names etc.
        """
        csv_data = self.get_csv_data("hse_deviationCSV")
        return csv_data

    def get_workers(self) -> list[dict]:
        """
        :return: List of workers with names, ids etc.
        """
        workers = self.get_csv_data("tilsettCSV")
        return workers

    def get_projects(self, include_inactive: bool = False) -> list[dict]:
        """
        Gets project data from Proresult.
        :param include_inactive: If True, include inactive/closed projects (taMedAvslutta=1)
        :return: List of projects as dictionaries
        """
        query_params = {}
        if include_inactive:
            query_params["taMedAvslutta"] = 1

        projects = self.get_csv_data("prosjektCSV", query_params)
        return projects

    def get_customers(self) -> list[dict]:
        """
        :return: List of customers
        """
        customers = self.get_csv_data("kundeCSV")
        return customers

    def get_images(self, deviation_id: int) -> dict:
        """
        :param deviation_id: The id of the deviation to get images for
        :return: Dict with filename as key and url as value
        """
        url = self.api_url + f"?fn=hentBilder&hse_deviationId={deviation_id}"
        response = requests.get(url, headers=self.headers, timeout=60)

        if response.status_code >= 300:
            raise Exception(f"Error getting images, bad status code: {response.status_code} {response.text}")

        # Doesn't pass encoding header correctly, but it's utf-8
        xml_data_raw = response.content.decode("utf-8")

        # Alternate error condition, they still send us 200 OK so we need to check the body
        if "TMCAPI - ingen tilgang" in xml_data_raw:
            raise Exception(f"Error getting image XML data, no access: {response.text}")

        images = {}

        # Parse xml data (fromstring takes a, uh, bytes-like object and not a string)
        root = et.fromstring(response.content)
        xml_images = root.xpath("/Bilder/Bilde")

        for image in xml_images:
            url = image.find("Url").text
            filename = image.find("Filnavn").text

            if filename in images:
                logging.warning(f"In PR deviation {deviation_id} image {filename} is duplicate, skipping")
                continue

            images[filename] = url

        return images
