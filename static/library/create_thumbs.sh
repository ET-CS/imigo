#!/bin/bash

workdir=/websites/imigo/static/library
cd $workdir

for folder in `ls -D`; do
    echo $folder;
    cd $workdir/$folder;
    for i in *.jpg; do
	if [[ $i == *"thumb"* ]]
	then
	    echo "Thumb file"
	else
	    echo $i;
	    convert $i -resize x250 $(basename $i .jpg).thumb.jpg;
	fi
    done
    cd $workdir;
done

optimize() {
  jpegoptim *thumb.jpg --strip-all
# 2 years of your life:
  #optipng -o 7 *.png
  for i in *
  do
    if test -d $i
    then
      cd $i
      echo $i
      optimize
      cd ..
    fi
  done
  echo
}
optimize
