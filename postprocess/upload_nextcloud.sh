#!/bin/bash
set -e
set -u

FILE=$1
basename=$(basename $FILE)

curl -T $FILE -u "${NC_USER}:${NC_PASS}"\
     "${NC_BASEURL}/remote.php/dav/files/${NC_USER}/${NC_DIR}/${basename}"
rm $FILE
