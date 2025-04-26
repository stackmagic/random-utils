#!/bin/bash

# config
SESSION_NAME="my_session"
INTERVAL=0.2
TIMEOUT="300s"
IFC="eno1"

# set cpu to performance governor
echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# clear logfile
> log.txt

# launch stress-ng and kill tmux session when done
tmux new-session -d -s $SESSION_NAME
tmux send-keys -t $SESSION_NAME:0 "stress-ng --cpu 0 --cpu-method all --timeout $TIMEOUT --metrics-brief ; tmux kill-session -t $SESSION_NAME" C-m

# collect temperature data
tmux new-window -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME:1 "watch -n${INTERVAL} 'sensors | grep Package | cut -d: -f2 | cut -dC -f1 | tee -a log.txt'" C-m

# run s-tui if available
if command -v s-tui >/dev/null 2>&1; then
	tmux new-window -t $SESSION_NAME
	tmux send-keys -t $SESSION_NAME:2 "s-tui" C-m
fi

# Attach to the tmux session
tmux attach-session -t $SESSION_NAME

sort -n log.txt | uniq -c > chart.txt

python3 draw_chart.py chart.txt

mv chart.txt chart-$(cat /sys/class/net/${IFC}/address | sed 's/://g')-$(date +%s%3N).txt


