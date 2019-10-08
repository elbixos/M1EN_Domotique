cd ../Sources
source ./_makeindex
cd ../Cours
source ./_makeindex
source ./generateFullLesson.sh

echo "generation pdf"
pandoc cours.md -o cours.pdf
