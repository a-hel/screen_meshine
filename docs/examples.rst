Examples
========

The ``projects`` folder contains 3 example of already scraped data that you can use to get acquainted with the grapher.

Example 1
---------

This Example contains scraped terms from the keywords *virus*, *bacteria*, *infection*, *flu*, *influenza*, *common cold*, and *fever*. Make a graph including only certain MeSH categories:

>>> ./MedCrawler.sh  p -pr Example1 -mw 10 B01.650 B03 B04 C01 C02 D

Example 2
---------

These terms come from WordPress searches for the keywords *insomnia*, *sleepless* and *sleeping disorder*. Exclude the term 'Id' with the following syntax:

>>> ./MedCrawler.sh  p -pr Example2 -mw 5 /Id

Example 3
---------

Here, you can visualize associations with the higlighted term *Headache* through the following example:

>>> ./MedCrawler.sh p -pr Example3 -hl Headache -mw 10