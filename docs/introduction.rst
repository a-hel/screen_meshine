Introduction
============

MedCrawler is a lightweight tool to analyze the public's perception of medical concepts. It retrieves blog posts about certain topics and extracts medical terms from them in order to find relevant connections.

The tool contains three sub-modules for different parts of the workflow, which can be used in conjunction or alone.

The **Scraper** looks for blog posts according to user-specified tags. Different plugins allow to include different sources in the search.

The **Indexer** is a wrapper for the `NLM Medical Text Indexer API <https://ii.nlm.nih.gov/Web_API/index.shtml>`_. This step exctracts the medically relevant words and returns them as `MeSH <https://en.wikipedia.org/wiki/Medical_subject_headings>`_ terms.

Finally, the **Grapher** analyzes the occurrence of the terms in the various blog posts and presents the correlations in a network graph.