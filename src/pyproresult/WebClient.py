import logging

import requests


class WebClient:
    def __init__(self, base_url, username, password, dbname):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.dbname = dbname
        self.session = requests.Session()
        self.verbose = False

        self.login()

    def login(self):
        """
        Logs in to the Proresult website using the provided payload.
        :raises Exception: If the login fails.
        :return: The status code of the login request.
        """

        payload = {
            'username': self.username,
            'pass': self.password,
            'dbname': self.dbname
        }

        response = self.session.post(f'{self.base_url}/userlogin.php', data=payload)

        if response.status_code == 200:
            logging.debug(f'Proresult website login successful')
            logging.debug(response.text) if self.verbose else None
        else:
            logging.error(response.text)
            raise Exception(f'Proresult website login failed: {response.text}')

        return response.status_code
