#!/bin/bash
FILES="/mnt/ubna_data_01/recover-20220822/UBNA_003/*.WAV"
for f in $FILES
do
  echo "Processing $f..."
  cd ~/opt/Raven-1.5.0.0043
  ./Raven "$f" -viewPreset:"Default" -detType:"Band Limited Energy Detector" -detPreset:"LFBatCallDetector" -detTable:"/home/aditya/union-bay-bats/results/2022_field_summary/recover-20220822-003-detect/lf_<f>" &
  sleep 90
  killall -9 Raven
done
