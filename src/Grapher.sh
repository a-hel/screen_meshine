#!/bin/sh


usage=" 
  Usage:
  ./Grapher.sh <cat1> <cat2> -p project /<exclude>

  Options:
  -mw, --minimumweight \t Minimum weight of edges
  -hl, --highlight \t Highlight term
  -h, --help \t\t Display this help

  Example:
  ./Grapher.sh B01 B02 C -p NewProject -mw 10 /Humans /Cats

  Check out the online documentation.
  "


pycommand="correlate.py $@"
hasProject=false

if [ "$#" -le 0 ]; then
	echo "$usage"
	exit 0
fi
# Argument loop


while [ "$1" != "" ]; do
    case $1 in
        -h | "?" | --help ) echo "$usage"
							exit 0
                            ;;
        -p | --project )    hasProject=true
							shift
                            ;;
    * )                     shift
                            ;;
    esac
    
done

if $hasProject ; then
    python $pycommand
else
	echo "No project specified."
	echo "Use -p to specify project or -h for help."
	exit 0
fi