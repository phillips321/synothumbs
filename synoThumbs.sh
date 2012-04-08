#!/bin/bash
# Author:	phillips321 contact through phillips321.co.uk
# License:	CC BY-SA 3.0
# Use:		
# Released:	www.phillips321.co.uk
    version=0.1
# ChangeLog:
#	v0.1 - first release

XLname="SYNOPHOTO:THUMB_XL.jpg" ; XLsize="1280x1280";
Lname="SYNOPHOTO:THUMB_L.jpg" ; Lsize="800x800";
Bname="SYNOPHOTO:THUMB_B.jpg" ; Bsize="640x640";
Mname="SYNOPHOTO:THUMB_M.jpg" ; Msize="320x320";
Sname="SYNOPHOTO:THUMB_S.jpg" ; Ssize="160x160";
ORIGIFS=$IFS ; IFS=$(echo -en "\n\b")

makeline(){ printf "%${1:-$COLUMNS}s\n" ""|tr " " ${2:-#;};}
#intro
makeline; echo " Welcome to synoThumb.sh version $version"; echo " This script creates the thumbs for a synology"; makeline;

#help message
if [[ $# == 0 ]] ; then makeline; echo " Error: What directory to process?"; echo " Usage: $0 ."; makeline ; exit 1; fi

#main block
for i in `find ${1} \( -type f -a \( -name "*.JPG" -o -name "*.jpg" -o -name "*.png" -o -name "*.PNG" -o -name "*.jpeg" -o -name "*.JPEG" \) ! -path "*@eaDir*" \)`
do
  picName=`echo "${i}" |  awk -F\/ '{print $NF}'`
  picDir=`echo "${i}" | sed s/"${picName}"//g | sed s/.$//`
  echo "Searching Thumbs For $i"
  [[ !(-d "$picDir"/"@eaDir"/"$picName") ]] && (mkdir -p "$picDir""/@eaDir/""$picName"; chmod 775 "$picDir"/"@eaDir"/"$picName";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$XLname") ]] && (convert -size $XLsize "$picDir""/""$picName" -resize $XLsize -auto-orient -flatten "$picDir"/"@eaDir"/"$picName"/"$XLname"; echo "   -- "$XLname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Lname") ]] && (convert -size $XLsize "$picDir""/@eaDir/""$picName""/""$XLname" -auto-orient -resize $Lsize "$picDir""/@eaDir/""$picName""/""$Lname"; echo "   -- "$Lname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Bname") ]] && (convert -size $Lsize "$picDir""/@eaDir/""$picName""/""$Lname" -auto-orient -resize $Bsize "$picDir""/@eaDir/""$picName""/""$Bname"; echo "   -- "$Bname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Mname") ]] && (convert -size $Bsize "$picDir""/@eaDir/""$picName""/""$Bname" -auto-orient -resize $Msize "$picDir""/@eaDir/""$picName""/""$Mname"; echo "   -- "$Mname" thumbnail created";)
  [[ !(-f "$picDir"/"@eaDir"/"$picName"/"$Sname") ]] && (convert -size $Msize "$picDir""/@eaDir/""$picName""/""$Mname" -auto-orient -resize $Ssize "$picDir""/@eaDir/""$picName""/""$Sname"; echo "   -- "$Sname" thumbnail created";)
done

#exit message
makeline; echo " Now log into DSM and reindex your photos"; echo " (Control Panel --> Media Indexing Service --> Re-index)"; makeline;

IFS=$ORIGIFS;
exit 0