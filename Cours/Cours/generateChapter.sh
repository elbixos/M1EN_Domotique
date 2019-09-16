#!/bin/bash
NumChap=$1
FILE=0${NumChap}_cours${NumChap}.md
echo "generation du fichier "$FILE


if [ -f $FILE ]; then
    \rm $FILE
fi

cat 0${NumChap}_*.md returnSommaire.md > $FILE
