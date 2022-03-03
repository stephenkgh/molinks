#!/bin/bash
# update dotfiles in docker-mounted homedir

SOURCE=$HOME/projects/dotfiles/docker
DEST=./web-home

if [ -d $DEST ] ; then
    for x in $SOURCE/* ; do cp -v $x $DEST/.$(basename $x) ; done
fi
