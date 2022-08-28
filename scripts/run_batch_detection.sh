#!/bin/bash
f=$"/mnt/ubna_data_01/recover-20220822/UBNA_001/20220821_000000.WAV"
echo "Processing $f..."
cd ~/opt/Raven-1.5.0.0043
./Raven "$f" -viewPreset:"Default" -detType:"Band Limited Energy Detector" -detPreset:"LFBatCallDetector" -detTable:"/home/aditya/union-bay-bats/results/2022_field_summary/recover-20220822-001-detect/lf_<f>" &
PID=$!
sleep 10
kill $PID
