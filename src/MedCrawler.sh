#!/bin/sh

src_dir=../src/
project_dir=../bin/
plugins=()
searchterms=()

usage=" \n \n
Usage: \n \n

no parameters: \t		Start program in quickstart mode \n
 -h, --help: \t\t		Display this help \n
-pr, --project: \t	Unique project identifier \n
-pl, --plugins: \t	Plugins to include in search \n
-t, --terms: \t\t		Search terms for this project \n
-n, --number: \t\t		Number of posts to retrieve per plugin and term \n
 \n
Check out the online documentation. \n \n"


# Quickstart mask

if [ $# -lt 1 ]; then
    echo "*********************************"
    echo "**    MedCrawler Quickstart    **"
    echo "*********************************"
    echo ""
    echo ""
    read -p "Enter project name: " project
    echo ""
    read -p "Enter the plugins you want to use, separated by whitespace.: " plugins
    echo ""
    echo "Enter the search terms, separated by whitespace."
    echo "If the search term contains a whitespace, replace it with a plus sign."
    echo "Example: Search terms: motorbike car+insurance"
    read -p "Search terms: " searchterms
    echo ""
    read -p "Chose how many entries to retrieve per term and plugin: " n_terms
    echo ""
    read -p "Do you want to run the program now (yes/no/help): " status
    case $status in
    	yes | y | 1 | true ) 	echo Starting project $project
								;;
		help | h | ? )			echo $usage
								exit 0
								;;
		* )						exit 0
	esac
    py_string="crawl -to $res_dir -p $plugins $n_terms $searchterms"
else
	py_string=$@
fi


# Invoke python scraper

python -m cProfile main.py $py_string
