import requests
import json


class Printer:

    def __init__(self, api_key):
        self.url = 'http://127.0.0.1:8000'
        self.api_key = api_key
        self.folder = '.\\pdf\\'

    def get_checks(self):
        response = requests.get(f'{self.url}/checks/{self.api_key}')
        self.checks = response.json()

    def download_pdf(self):
        for check in self.checks:
            r = requests.get(self.url + check['pdf_file'])
            open(self.folder + check['pdf_file'].split('/')
                 [-1], 'wb').write(r.content)
            self.print_check(check)

    def print_check(self, check):
        print(self.folder + check['pdf_file'].split('/')[-1])
        requests.post(self.url + f'/print/{check["id"]}')


cp1 = Printer('CP1qwerty')
cp1.get_checks()
cp1.download_pdf()
