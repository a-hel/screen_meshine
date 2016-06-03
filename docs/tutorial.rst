Tutorial
========

Quickstart
----------

In the terminal, navigate to the location of the tool. Then, change to the ``/src`` folder.

>>> cd src

To start the program in quickstart mode, just run the shell script:

>>> ./run.sh

This will start the Scraper and send the results directly to the Indexer.

You will be prompted to enter the scraping parameters and your UMLS credentials.

**Project:** A unique project name to save your results

**Username:** Your UMLS username. If you don't have a username, refer to the installation section on how to request one.

**Password:** Your UMLS password

**E-mail:** Your e-mail address

**Plugins:** List the plugins you want to use for the web search. Standard pre-installed plugin is wp (WordPress). If you want to use more than one plugin, separate their names by a whitespace.

**Search terms:** List the search terms for your project. Separate the search terms by a whitespace. If your search term contains any whitespaces, replace them with a plus sign (+). Example: ``car+insurance motorbike``

**Number of entries:** List the number of entries you want to retrieve for each search term and each plugin.

Confirm the start of the program with (y)es

.. note:: It takes around 15 and 30 seconds to process a blog post, so this might take a while if you retrieve a large number of posts. In future versions, this might be accelerated by using parallel requests.

.. important:: The script has to be invoked directly from the ``/src`` folder.

Command line tool
-----------------

Instead of quickstart, you can use command line parameters to start the program:

| no parameters:        Start program in quickstart mode (see above)
| -h, --help:        Display the help 
| -pr, --project:   Unique project identifier
| -u, --username:  Your UMLS username
| -pw, --password: Your UMLS password
| -e, --email:        A valid e-mail address
| -pl, --plugins:   Plugins to include in search, separated by whitespace
| -t, --terms:       Search terms for this project, separated by whitespace. 	*Whitespaces within the search terms need to be replaced by a plus sign (+)*
| -n, --number:      Number of posts to retrieve per plugin and term \n

You start the crawler as follows:

.. Example:: 
>>> ./run.sh -pr NewProject -u Username -pw Password -e Your@email.com -pl plugin1 plugin2 -t tag1 tag2 tag3 -n 200

Analysing the results
---------------------

The result analysis is done via command line. Still in the ``src`` folder, run

>>> ./Grapher.sh

With the following mandatory parameters:

| -p, --project: The project name assigned in the previous step
| -mw, --minweight: The minimum weight of connections to be displayed. The higher the number, the more non-relevant results are excluded

The following parameters are optional:

| -hl, --highlight: Only show connections with a certain term. Make sure to use the exact, case-sensitive MeSH spelling
| -c, --colors: Currently not implemented

List the MeSH categories you wish to include. You can define the depth of filtering by typing the first characters of the tree number. You can find the category codes on the `MeSH website <https://www.nlm.nih.gov/cgi/mesh/2016/MB_cgi>`_.

To exclude certain terms, prepend a forward slash (/).

.. Example::
 >>> ./Grapher.sh -p NewProject -mw 10 A B C01 /Humans

Check out the example section for more examples

.. important:: When excluding certain terms, make sure that the spelling matches the official MeSH spelling (including case-sensitivity).

What happens under the hood: The program generates the network graph according to your parameters. Play around with the parameters until you are happy with the result. The graph is saved as a png file in the ``/projects`` directory, so you can access it later. A log file with the same name is also stored. It contains all the drawn edges, as well as the command used to create the graph.
