#!/bin/sh
# Simple script to start bot in background
screen -d -m -S albinobot -L -Logfile albinobot.log python3 ./albinobot.py