#!/bin/bash

FILE=cours.md
if [ -f $FILE ]; then
    \rm $FILE
fi

# generation des chapitres independants
source generateChapter.sh 1

## generation du fichier complet.
LISTE=$(ls 000_title.md 00_intro.md 0*_0*.md 98_liens.md)
echo "---------------"
echo "Liste des fichiers du cours complet"
echo ""
echo $LISTE
cat $LISTE > ../cours.md
echo "---------------"
