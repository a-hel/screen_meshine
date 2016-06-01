#!/bin/sh


usage=" \n \n
Usage: \n \n

./Grapher.sh <cat1> <cat2> -p project !<exclude>\n
Options:\n
-mw, --minimumweight \t Minimum weight of edges\n
-hl, --highlight \t Highlight term\n
-h, --help \t\t Display this help\n
Example:\n
./Grapher.sh B01 B02 C -p NewProject -mw 10 !Humans !Cats
 \n
Check out the online documentation. \n \n"


pycommand="correlate.py $@"
echo $pycommand
# Argument loop
while [ "$1" != "" ]; do
    case $1 in
        
        -h | ? | --help )   echo $usage
							exit 0
                            ;;
    * )                     echo "*"
                            shift
                            ;;
    esac
    
done

echo "$pycommand"
python $pycommand