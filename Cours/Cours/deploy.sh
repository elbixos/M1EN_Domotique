cd Sources
source ./_makeindex
cd ../Cours
source ./_makeindex
source ./generateFullLesson.sh
pandoc cours.md -o cours.pdf
