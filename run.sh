#!/bin/sh
bin_dir=../bin/
api_dir=SKR_Web_API_V2_1
usage="nada"
plugins=()
searchterms=()

if [ $# -lt 1 ]; then
    echo "*********************************"
    echo "**           WELCOME           **"
    echo "*********************************"
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
    
else
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

            -h | --help )       echo $usage
								shift
                                ;;
        * )                     shift
        esac
        
    done
fi

res_dir=../projects/$project
mkdir $res_dir

py_string="-to $res_dir -p $plugins $n_terms $searchterms"
echo $py_string
python scraper.py $py_string

res_files=($res_dir/res_*)
infiles=${res_files[@]}
echo $infiles



BASEDIR=$api_dir

CP=$BASEDIR/lib/httpclient-4.1.1.jar:$BASEDIR/lib/httpclient-cache-4.1.1.jar
CP=$CP:$BASEDIR/lib/httpcore-4.1.jar:$BASEDIR/lib/httpcore-nio-4.1.jar
CP=$CP:$BASEDIR/lib/httpmime-4.1.1.jar
CP=$CP:$BASEDIR/lib/commons-logging-1.1.1.jar
CP=$CP:$BASEDIR/lib/skrAPI.jar
CP=$CP:./

#infiles="$res_dir/res_1.txt $res_dir/res_2.txt"
outfiles=$res_dir/out.txt

cd $bin_dir
java -cp $BASEDIR/classes:$CP JobSubmitter $username $password $email $outfiles $infiles