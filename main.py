import requests
from bs4 import BeautifulSoup
import pandas as pd


class TheManifestSoup:

    def __init__(self):

        self.data = {}
        columns = ['id', 'prize', 'employees', 'industries', 'location', 'summary']
        for column in columns:
            self.data[column] = []
        self.source = None
        self.soup = None

    def init_soup(self, url_init):
        self.source = requests.get(url_init).text
        self.soup = BeautifulSoup(self.source, 'lxml')

    def write_to_excel(self):
        df = pd.DataFrame.from_dict(self.data, orient='index').transpose()
        df.to_excel(r'/Users/leonhagemann/PycharmProjects/project_papa/export_dataframe.xlsx')

    def get_items(self):

        for content in self.soup.find_all('article', class_='provider-profile'):
            try:
                id = content.get('id')
                body = content.find_all('div', class_='provider-basics-item-label')
                prize = None
                employees = None
                for item in body:
                    if "$" in item.text:
                        prize = item.text
                    elif "Employees" in item.text:
                        employees = item.text
                industries = []
                industries_tmp = content.find_all('div', class_='provider-industries-item')
                for industry in industries_tmp:
                    industries.append(industry.get("data-original-title"))
                location = content.find('span', class_='comp-addr').text
                try:
                    summary = content.find('div', class_='provider-summary').p.text
                except:
                    summary = content.find('div', class_='provider-summary').text

                if id is not None and prize is not None and employees is not None and \
                        industries is not None and location is not None and summary is not None:
                    self.data['id'].append(id)
                    self.data['prize'].append(prize)
                    self.data['employees'].append(employees)
                    self.data['industries'].append(industries)
                    self.data['location'].append(location)
                    self.data['summary'].append(summary)

            except Exception as e:
                print("Could not fetch items due to error :", e)


soup = TheManifestSoup()
for i in range(0, 13):
    soup.init_soup(f'https://themanifest.com/de/software-development/companies?page={i}')
    soup.get_items()

soup.write_to_excel()
