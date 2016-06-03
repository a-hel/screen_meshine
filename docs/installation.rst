Installation
============

Requirements
------------

You need Python 2.7 and Java.

Get MedCrawler
--------------

MedCrawler is available from Github (.. __:https://github.com/a-hel/MedCrawler/releases/latest ).

First, download the *Sources.zip* and unzip it to the location of your choice.

Then, download the file *Indexer.class* and save it in the */bin* folder of the MedCrawler directory

Get the Web API
---------------

The module relies on the UMLS Web API for MeSH term extraction. In order to use it, you need to apply for a free UMLS license. Approval of your request can take up to three days.

Sign up for an UMLS license at .. __:https://uts.nlm.nih.gov/home.html
Once your request is approved, you will recieve your UMLS username and password that you will need to start the scraper.

Afterwards, download the NLM Medical Text Indexer API at .. __:https://ii.nlm.nih.gov/Web_API/index.shtml

Unzip the *jar* archive and copy the unzipped folder into the */bin* directory. Make sure the folder is named "SKR_Web_API_V2_1" and rename if necessary.

.. note:: To get the most recent version, you can clone the repository
	>>> git clone https://github.com/a-hel/MedCrawler.git

	Then, copy the Web API to the */bin* folder.
	Last, compile the *Indexer*:
	>>> ./src/compile.sh

