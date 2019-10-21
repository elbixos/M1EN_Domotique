cd ../Sources
source ./_makeindex
cd ../Cours
source ./_makeindex
source ./generateFullLesson.sh

echo "generation pdf"
pandoc cours.md -o cours.pdf -V geometry:papersize=a4 -V geometry:margin=1in
