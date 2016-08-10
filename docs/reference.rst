Reference
=========

mc_scraper
----------

.. function:: main(tags, n_posts[, plugins=('wp'), target="new_project"])

	Retrieve blog posts and yield them as pure ASCII.


	:param tags: Keywords to look for
	:type tags: list of str
	:param n_posts: Number of posts to retrieve per keyword and plugin
	:type n_posts: int
	:param plugins (list of str): Plugins to include. Plugins must be saved
		in the 'plugins' folder under <plugin_name>.py
	:type plugins: list of str
	:param target: Project name
	:type target: str
	:rtype: list of str
	

mc_indexer
-----------

.. function:: build_index(sourcefile)

	Build index based on sourcefile and return first node.

	:param sourcefile: Path and file name of the MeSH database (e.g. 
		desc2016.xml)
	:type sourcefile: str
	:rtype: mc_tree.Node

.. function:: traverse(index, posts)

	Find indexed words from posts and return the preferred term and its tree number

	:param index: The tree node from where to start the search
	:type index: mc_tree.Node
	:param posts: List of all the posts in pure ASCII
	:type posts: list of str
	:rtype: list of tuples of str


mc_grapher
-----------

.. function:: main(project[, categories=[], minweight=1, highlight=False, exclude=[], color_scheme="default", source="terms.txt"])

	Build and show the graph.

	:param project: The project name
	:type project: str
	:param categories: The MeSH categories to include. If
	    the list is empty, all categories will be included.
	:type categories: list of str
	:param minweight (int, default=1): Minimum weight necessary for connections
	    to be displayed.
	:type minweight: int
	:param highlight (str, default=False): A specific term to highlight. If
	    false, no term will be highlighted
	:type highlight: str
	:param exclude: List of terms to exclude from the analysis.
	:type exclude: list of str
	:param color_scheme: Color scheme for the plot, not implemented
	:type color_scheme: str
	:param source: Name of sourcefile within project
	    folder
	:type source: src
	:rtype: None


.. function:: build_matrix(res_file[, categories=[], highlight=False, exclude=[],
    color_scheme="default"])

    Build and return the correlation matrix and node labels and their colors

	:param res_file: File name and path to load
	:type res_file: str
	:param categories: List of categories to include
	:type categories: list of str
	:param highlight: MeSH term to highlight
	:type highlight: str
	:param exclude: List of MeSH terms to exclude
	:type exclude: list of str
	:param color_scheme: Color scheme for the plot, not implemented
	:type color_scheme: str
	:rtype: scipy.sparse.dok_matrix, list of str, list of str


.. function:: create_plot(corr_map, terms, colors[, minweight=1, dpi=600])

	Draw plot and create metadata.


	:param corr_map: Correlation matrix as returned from build_matrix()
	:type corr_map:  scipy.sparse.dok_matrix
	:param terms: List of unique terms in the same order as the
	    corrmap axes
	:type terms:  list of str
	:param colors: List of colors according to MeSH category in the
	     same order as the corrmap axes
	:type colors:  list of str
	:param minweight: Minimum number of co-occurrences to draw.
	:type minweight: int
	:param dpi: DPI for plot
	:type dpi: int
	:rtype: Matplotlib.Figure, list of str, list of str

