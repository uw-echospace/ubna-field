#!/bin/sh

# Sync direct uploaded data to the backup mirror
rsync -nahvP /mnt/ubna_data_01 /mnt/ubna_data_01_mir/
