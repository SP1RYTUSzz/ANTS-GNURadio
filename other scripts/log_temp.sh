#!/bin/bash

LOGFILE="$HOME/pi_temp_log.txt"

echo "Timestamp,Temperature_C" | tee -a "LOGFILE"

while true
do
	TIME=$(date +"%Y-%m-%d %H:%M:%S")
	TEMP=$(vcgencmd measure_temp | cut -d= -f2 | cut -d "'" -f1)

	echo "$TIME,$TEMP" | tee -a "$LOGFILE"

	sleep 1
done