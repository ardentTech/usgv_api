from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import requests


class Spider(object):

    url = None

    def crawl(self):
        raise NotImplementedError

    def get_html(self, url=None):
        _url = url or self.url
        return BeautifulSoup(requests.get(_url).content, "html.parser")


class TableSpider(Spider):

    table_attrs = {}
    table = None

    def __init__(self):
        self._column_names = []
        self._row_data = OrderedDict()

    @property
    def column_names(self):
        return self._column_names

    @property
    def row_data(self):
        return self._row_data.values()

    def get_body(self):
        return self.table.find("tbody")

    def get_body_rows(self):
        return self.get_body().find_all("tr")

    def get_cells(self, row):
        return row.find_all("td")

    def get_cell_text(self, cell):
        return self.get_text(cell)

    def get_column_names(self):
        return list(map(
            lambda header: self.get_header_cell_text(header), self.get_header_cells()))

    def get_header_cells(self):
        return self.table.find_all("th")

    def get_header_cell_text(self, cell):
        return self.get_text(cell)

    def get_row_data(self, row):
        return list(map(
            lambda cell: self.get_cell_text(cell), self.get_cells(row)))

    def get_table(self, html):
        return html.find("table", attrs=self.table_attrs)

    def get_text(self, a):
        return a.text


class PaginatedTableSpider(TableSpider):

    def get_next_page(self):
        raise NotImplementedError


class MassShootingSpider(PaginatedTableSpider):

    table_attrs = {"class": "responsive sticky-enabled"}
    url_template = "http://www.gunviolencearchive.org/reports/mass-shooting?page=0&year={0}"

    def __init__(self, year):
        self.url = self.url_template.format(year)
        super(MassShootingSpider, self).__init__()

    def crawl(self):
        url = self.url
        fresh = True

        while fresh:
            self.table = self.get_table(self.get_html(url=url))
            if url == self.url:  # only on first page
                self._column_names = self.get_column_names()
            for index, row in enumerate(self.get_body_rows()):
                data = self.get_row_data(row)
                uid = data[-1]
                if (index == 0 and uid in self._row_data):
                    fresh = False
                    break
                self._row_data[uid] = data
            if fresh:
                url = self.get_next_page(url)

    # @todo this might be trying to do too much...
    # @todo maybe have a method named `get_uid`???
    def get_cell_text(self, cell):
        try:
            return cell.ul.li.a.get("href").split("/")[2]
        except:
            return super(MassShootingSpider, self).get_cell_text(cell)

    def get_header_cell_text(self, header):
        if header.a is not None:
            header = header.a
        return super(MassShootingSpider, self).get_header_cell_text(header)

    def get_next_page(self, url):
        current = int(re.search(r'page=(\d+)', url).group(1))
        return re.sub(r'page=\d+', 'page={0}'.format(current + 1), url)
