Creating your own plugins
=========================

The MedCrawler is shipped with the WordPress plugin, which accesses blogs hosted with WordPress through their API. While this is probably the largest repository of blogs, you might want to include other sources as well.

You can extend the functionality of the module by writing your own plugins. A plugin is a short python script that will be loaded and executed during the scraping. For security reasons, only include plugins that you fully understand.

A plugin must be saved in the */plugins* folder. When invoked, the crawler calls the plugin's ``main()`` function with a list of terms and number of entries as arguments.

>>> plugin.main(['term1', 'term2', 'term3'], size=200)

The main function returns, or even better yields, the retrieved blog posts as an iterable

Save the script in the *src/plugins/* folder. Use the filename (without the *.py extension) to access the plugin. Feel free to share your plugin with a pull request to github.