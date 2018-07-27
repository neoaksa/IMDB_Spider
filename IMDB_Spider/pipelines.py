# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from IMDB_Spider.movie_item import MovieItem, MovieReview
from scrapy.exporters import CsvItemExporter
import csv
import os

class Pipeline(object):
    # def __init__(self):
    #     self.exporter = None
    #     self.file = None
    #
    # def close_spider(self,spider):
    #     for exporter in self.exporter.value():
    #         exporter.finish_exporting()
    #         exporter.file.close()
    def __init__(self):
        # remove if exists output files
        try:
            os.remove('MovieItem.csv')
        except OSError:
            pass

        try:
            os.remove('MovieReview.csv')
        except OSError:
            pass

    def process_item(self, item, spider):
        if isinstance(item,MovieItem):
            self.handleMovieItem(item)

        if isinstance(item,MovieReview):
            self.handleMovieReview(item)

    def handleMovieItem(self,item):
        with open('MovieItem.csv', "a") as file:
            w = csv.DictWriter(file, item.__dict__['_values'].keys())
            # w.writeheader()
            w.writerow(item.__dict__['_values'])

    def handleMovieReview(self,item):
        with open('MovieReview.csv', "a") as file:
            w = csv.DictWriter(file, item.__dict__['_values'].keys())
            # w.writeheader()
            if item['id']:
                w.writerow(item.__dict__['_values'])
