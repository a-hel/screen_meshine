Tutorial
========

Quickstart
----------

In the terminal, navigate to the location of the tool. Then, change to the ``/src`` folder.

>>> cd src

To start the program in quickstart mode, just run the shell script:

>>> ./MedCrawler.sh

or 

>>> bash MedCrawler.sh

depending on your operating system.

This will start the Scraper and send the results directly to the Indexer.

You will be prompted to enter the scraping parameters.

**Project:** A unique project name to save your results

**Plugins:** List the plugins you want to use for the web search. Standard pre-installed plugin is wp (WordPress). If you want to use more than one plugin, separate their names by a whitespace.

**Search terms:** List the search terms for your project. Separate the search terms by a whitespace. If your search term contains any whitespaces, replace them with a plus sign (+). Example: ``car+insurance motorbike``

**Number of entries:** List the number of entries you want to retrieve for each search term and each plugin.

Confirm the start of the program with (y)es

.. note:: Data for each project will be stored in the ``../projects/`` folder.

Command line tool
-----------------

Instead of quickstart, you can use command line parameters for crawling and plotting. Behaviour depends on the first parameter, which has to be (c)rawl or (p)lot:

Crawl mode parameters (arbitrary order):

| -pr, --project:   Unique project identifier
| -p, --plugins:   Plugins to include in search, separated by whitespace	*Whitespaces within the search terms need to be replaced by a plus sign (+)*

Any other input will be interpreted as search keyword or number of terms (if numeric)

.. Example:: 
>>> ./MedCrawler.sh c -pr Example3 2000 -p wp pain migraine headache

Plotting mode parameters:

| -pr, --project: Unique project identifier
| -mw, --minweight: Minimum weights to plot
| -hl, --highlight (optional): Term to highlight in the plot. With this option, only connections with the specified term will be displayed. This is case-sensitive.

To exclude unwanted terms, prepend them with a slash ('/').

Every argument is interpreted as a category. You can define the depth of filtering by typing the first characters of the tree number. You can find the category codes on the `MeSH website <https://www.nlm.nih.gov/cgi/mesh/2016/MB_cgi>`_.

.. Example::
>>> ./MedCrawler.sh p -pr Example1 -mw 10 B01.650 B03 B04 C01 C02 D

.. note:: If you are not sure, which minweight setting will produce useful results, choose a large one (e.g. 1000). If it is too large to find any connections, you will get a summary of the weight distribution.

.. note:: You can also directrly call the ``main.py`` script with the same parameters. This way, you cannot use the quickstart mode.

