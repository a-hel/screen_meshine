#!/bin/sh

# Instructions for the Java compiler

BASEDIR=../bin/SKR_Web_API_V2_1

CP=$BASEDIR/lib/httpclient-4.1.1.jar:$BASEDIR/lib/httpclient-cache-4.1.1.jar
CP=$CP:$BASEDIR/lib/httpcore-4.1.jar:$BASEDIR/lib/httpcore-nio-4.1.jar
CP=$CP:$BASEDIR/lib/httpmime-4.1.1.jar
CP=$CP:$BASEDIR/lib/commons-logging-1.1.1.jar
CP=$CP:$BASEDIR/lib/skrAPI.jar

javac -cp $BASEDIR/classes:$CP -d ../bin/ Indexer.java

exit 0
