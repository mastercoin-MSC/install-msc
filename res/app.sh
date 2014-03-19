#!/bin/bash

kill_child_processes() {
	kill $SERVER_PID
	rm -f $LOCK_FILE
}

# Ctrl-C trap. Catches INT signal
trap "kill_child_processes 1 $$; exit 0" INT

APPDIR=`pwd`

DATADIR=$APPDIR/logs
LOCK_FILE=$DATADIR/msc_cron.lock
PARSE_LOG=$DATADIR/parsed.log
VALIDATE_LOG=$DATADIR/validated.log
ARCHIVE_LOG=$DATADIR/archived.log

if [ ! -d $DATADIR ]; then
	mkdir -p $DATADIR
fi

SERVER_PID=$!

while true
do

	# check lock (not to run multiple times)
	if [ ! -f $LOCK_FILE ]; then

		# lock
		touch $LOCK_FILE

		# parse until full success
		x=1 # assume failure
		echo -n > $PARSE_LOG
		while [ "$x" != "0" ];
		do
			python msc_parse.py 2>&1 >> $PARSE_LOG
  			x=$?
		done

		python msc_validate.py 2>&1 > $VALIDATE_LOG

		# update archive
		python msc_archive.py 2>&1 > $ARCHIVE_LOG

		mkdir -p www/tx www/addr www/general

	        cp tx/* www/tx
		cp addr/* www/addr
		cp general/* www/general

		# unlock
		rm -f $LOCK_FILE
	fi

	# Wait a minute, and do it all again.
	sleep 60
done
