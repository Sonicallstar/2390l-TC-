#!/bin/bash
# Script for saying the current local time
NOW=$(date +"Ground Control time is %M minutes past %l %p UTC")

echo $NOW 
pico2wave -w TimeTTS.wav "$NOW" && aplay TimeTTS.wav

