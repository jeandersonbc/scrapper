#!/usr/bin/env python3
import csv
import os
import re

from lxml import etree


class Entry:
    ALL_FIELDS = 'title description year url datasource filename'.split()

    def __init__(self, title, description, url, year, datasource):
        self.title = title
        self.description = description
        self.url = url
        self.year = year
        self.datasource = datasource
        self.filename = None

    def fields(self):
        return self.__dict__

    def __repr__(self):
        return repr(self.__dict__)


class IeeeHandler:
    @staticmethod
    def entries(node):
        return node.findall('//*[@class="List-results-items"]/xpl-results-item/div[1]')

    @staticmethod
    def extract_fields(node):
        title_node = node.find('./div/h2/a')
        description_node = node.find('./div/div/span')
        extracted_url = title_node.get('href')
        year_node = node.find('.//div[@class="description"]/div/span')
        year_only = re.sub('Year: ', '', normalize_text_node(year_node))
        return Entry(title=normalize_text_node(title_node),
                     description=normalize_text_node(description_node),
                     url=extracted_url,
                     datasource='ieee',
                     year=year_only)


class AcmHandler:
    @staticmethod
    def entries(node):
        return node.findall("//*[@id='results']/div[@class='details']")

    @staticmethod
    def extract_fields(node):
        title_node = node.find('./div[@class="title"]/a')
        description_node = node.find('./div[@class="abstract"]')
        extracted_url = title_node.get('href')

        source_node = node.findall("./div[@class='source']/span")
        year_node = source_node[0] if len(source_node) else None
        year_node = normalize_text_node(year_node)
        year_only = re.search('\d+', year_node).group()

        return Entry(title=normalize_text_node(title_node),
                     description=normalize_text_node(description_node),
                     url=extracted_url,
                     datasource='acm',
                     year=year_only)


class GoogleScholarHandler:
    @staticmethod
    def entries(node):
        return node.findall("//*[@id='gs_res_ccl_mid']/div[@class='gs_r gs_or gs_scl']")

    @staticmethod
    def extract_fields(node):
        title_node = node.find("./div[@class='gs_ri']/h3")
        title_anchor = title_node.find("./a")
        if title_anchor is not None:
            title_node = title_anchor

        description_node = node.find("./div[@class='gs_ri']/div[@class='gs_rs']")
        extracted_url = title_node.get('href')
        return Entry(title=normalize_text_node(title_node),
                     description=normalize_text_node(description_node),
                     url=extracted_url,
                     datasource="google-scholar",
                     year='0000')  # FIXME


def normalize_text_node(node):
    if node is None:
        return ""
    text = etree.tostring(node, method='text', encoding='utf-8', pretty_print=True).decode('utf-8')
    text = re.sub("(\s+|\\xa0)", " ", text).strip()
    return text.strip()


def read_html(input_file, handler):
    parsed_entries = []
    root_node = etree.parse(input_file, etree.HTMLParser())
    entries = handler.entries(root_node)

    for entry in entries:
        parsed_entry = handler.extract_fields(entry)
        parsed_entry.filename = os.path.basename(input_file)
        parsed_entries.append(parsed_entry)

    return parsed_entries


ENTRIES = []


def extractor(target_dir, handler):
    if not os.path.exists(target_dir):
        print('Path %s not found' % target_dir)
        return

    print('Checking %s' % target_dir)
    counter = 0
    for f in os.listdir(target_dir):
        input_path = os.path.join(target_dir, f)
        parsed_entries = read_html(input_path, handler)
        counter += len(parsed_entries)
        ENTRIES.extend(parsed_entries)
    print('Extracted %d entries' % counter)


extractor('html-acm', AcmHandler)
extractor('html-ieee', IeeeHandler)
extractor('html-google-scholar', GoogleScholarHandler)

with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=Entry.ALL_FIELDS, quotechar='"')
    writer.writeheader()
    writer.writerows(e.fields() for e in ENTRIES)

