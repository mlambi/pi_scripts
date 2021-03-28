#!/bin/bash

# script to receive video streamed to netcat and send it to mplayer
# sender command:  raspivid -b 4000000 -t 0 -o - | nc -l -p 5000

mplayer -x 1280 -y 720 -geometry 0:0 -fps 200 -demuxer h264es -noborder ffmpeg://tcp://10.0.0.58:5000
