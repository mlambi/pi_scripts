#!/bin/bash

# launch video stream using raspivid and netcat
# to receive:
# mplayer -x 1280 -y 720 -geometry 0:0 -fps 200 -demuxer h264es -noborder ffmpeg://tcp://x.x.x.x:5000

raspivid -b 4000000 -t 0 -o - | nc -l -p 5000
