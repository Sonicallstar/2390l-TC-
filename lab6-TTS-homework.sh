#!/bin/bash
#This is a shell script for lab 6 Homework Assignment
# Script for saying the current local time

#variable that includes the date and the string literal
Get_current_time=$(date +"The time is Currently %l:%M%p. Do you know where your children are?")

echo $Get_current_time

#commmand for generating a TTS file and incorporating the variable. This must show some variation from the one in class. 
pico2wave -w TimeH-M.wav "$Get_current_time"

#command for playing back the TTS audio file. This must show some variation from the one in class. 

aplay TimeH-M.wav
