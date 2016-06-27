#!/bin/sh


bin_dir=../bin/
api_dir=../bin/SKR_Web_API_V2_1
plugins=()
searchterms=()

usage=" \n \n
Usage: \n \n

no parameters: \t		Start program in quickstart mode \n
 -h, --help: \t\t		Display this help \n
-pr, --project: \t	Unique project identifier \n
-u, --username: \t	Your UMLS username \n
-pw, --password: \t	Your UMLS password \n
-e, --email: \t\t		A valid e-mail address \n
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
    read -p "Enter project name: " project
    read -p "Enter user name: " username
    read -p "Enter password: " -s password
    echo ""
    read -p "Enter e-mail address: " email
    read -p "Enter the plugins you want to use, separated by whitespace.: " -a plugins
    echo "Enter the search terms, separated by whitespace."
    echo "If the search term contains a whitespace, replace it with a plus sign."
    echo "Example: Search terms: motorbike car+insurance"
    read -p "Search terms: " -a searchterms
    read -p "Chose how many entries to retrieve per term and plugin: " n_terms
    read -p "Do you want to run the program now (yes/no/help): " status
    case $status in
    	yes | y | 1 | true ) 	echo Starting project $project
								;;
		help | h | ? )			echo $usage
								exit 0
								;;
		* )						exit 0
	esac
else
	# Argument loop
    while [ "$1" != "" ]; do
        case $1 in
            -pr | --project )    shift
                                project=$1
                                shift      
                                ;;
            -u | --username )   shift
                                username=$1
                                shift      
                                ;;
            -pw | --password )  shift
                                password=$1
                                shift      
                                ;;
            -e | --email )      shift
                                email=$1
                                shift      
                                ;;
            -n | --number )     shift
                                n_terms=$1
                                shift      
                                ;;
            -pl | --plugins )   shift
                                while [ "${1:0:1}" != "-" ] && [ "$1" != "" ]; do
                                    plugins+=$1
                                    plugins+=","
                                    shift
                                done
                                ;;
            -t | --terms )      shift
                                while [ "${1:0:1}" != "-" ] && [ "$1" != "" ]; do
                                    searchterms+=$1
                                    searchterms+=" "
                                    shift
                                    echo $1
                                done
                                
                                echo $1
                                ;;
            -h | ? | --help )   echo $usage
								exit 0
                                ;;
        * )                     shift
        esac
        
    done
fi

res_dir=../projects/$project
mkdir $res_dir
if [ $? == 1 ]; then
	echo "Project $project already exists."
	exit 1
fi

# Invoke python scraper
py_string="-to $res_dir -p $plugins $n_terms $searchterms"
python scraper.py $py_string

res_files=($res_dir/res_*)
infiles=${res_files[@]}

# Set variables for java
BASEDIR=$api_dir
CP=$BASEDIR/lib/httpclient-4.1.1.jar:$BASEDIR/lib/httpclient-cache-4.1.1.jar
CP=$CP:$BASEDIR/lib/httpcore-4.1.jar:$BASEDIR/lib/httpcore-nio-4.1.jar
CP=$CP:$BASEDIR/lib/httpmime-4.1.1.jar
CP=$CP:$BASEDIR/lib/commons-logging-1.1.1.jar
CP=$CP:$BASEDIR/lib/skrAPI.jar
CP=$CP:./

outfile=$res_dir/out.txt

# Invoke java indexer
cd $bin_dir
java -cp $BASEDIR/classes:$CP Indexer $username $password $email $outfile $infiles

echo "Retrieve leaf nodes..."

python leafer.py $outfile
echo "Data retrieval for $project done"