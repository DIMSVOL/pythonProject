import bs4
import requests as requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import yaml

with open("configs/config.yaml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


class TableScraper:
    """"Class for scraping data from given web page url"""
    url: str
    data: list
    column_names: list

    def __init__(self):
        self.url = cfg['urls']['table_url']
        self.data = []
        self.column_names = []

    def print_table(self) -> None:
        """Printing parsed data.
        :rtype: None
        """
        table = PrettyTable(self.column_names)
        for d in self.data:
            table.add_row(d.values())
        print(table)

    def find_tables(self) -> bs4.ResultSet:
        """Search for tables on the web page.
        :rtype: bs4.ResultSet
        """
        html = requests.get(self.url)
        soup = BeautifulSoup(html.text, 'html.parser')
        tables = soup.find_all('table')

        return tables

    def get_data_by_url(self) -> list:
        """
        Main function for parsing data
        :rtype list:
        """
        tables = self.find_tables()
        for n, table in enumerate(tables[:-1]):
            rows = table.find_all('tr')
            self.column_names = [r.text for r in rows[0].find_all('td')[:-1]]

            for i, r in enumerate(rows[1:]):
                elements = r.find_all('td')[:-1]
                elements_dict = {'operation': elements[0].text,
                                 'example': elements[1].text,
                                 'complexity': elements[2].text,
                                 'type': cfg['data_types'][n]
                                 }
                self.data.append(elements_dict)
            self.column_names.append('Type')
        return self.data
