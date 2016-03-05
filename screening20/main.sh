#!usr/bin/bash

scrapy crawl tagspider -o items.json

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

python cleanfile.py

python correlate.py