#Own plugins

You can extend the functionality of the module by writing your own plugins. This is handy if you wish to crawl other ressources than currently supported (i.e. WordPress).

A plugin is a short python script that will be loaded and executed during the scraping. For security reasons, only include plugins that you fully understand.

The tool calls the plugin's main() function and delivers a list of terms and number of entries.

plugin.main(['term1', 'term2', 'term3'], size=200)

The main function returns, or even better yields, the retrieved blog posts as a list or generator object. The results will be used as follows:

..Important::

The blog post must be ASCII-encoded and must not contain newlines. (This behavior may change in future reseases).

Save the script in the src/plugins/ folder. Use the filename (without the *.py) to access the plugin. Feel free to share your plugin with a pull request to github.