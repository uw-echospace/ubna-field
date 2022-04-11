# Union Bay Bat Monitoring

Our acoustic bat call data was gathered from two sites in the Union Bay Natural Area in Seattle, WA.

## Recording sites
- Carp Pond
- Foliage


## Recording Sessions
All dates and times were recorded in UTC and following ISO8601 format.

1) Carp Pond

Recording Session # | Start | End | Duration
--------------------|-------|-----|---------
1 | 2021-09-09T02:30Z | 2021-09-11T11:30Z | 57 hours
2 | 2021-09-20T23:00Z | 2021-09-21T08:30Z | 9.5 hours

2) Foliage

Recording Session # | Start | End | Duration
--------------------|-------|-----|---------
1 | 2021-09-09T02:00Z | 2021-09-09T23:00Z | 21 hours
2 | 2021-09-16T00:00Z | 2021-09-16T09:30Z | 9.5 hours
3 | 2021-10-01T02:00Z | 2021-10-03T10:30Z | 56.5 hours
4 | 2021-10-15T18:00Z | 2021-10-17T11:30Z | 41.5 hours

## Recording parameters
- Activity table uses HH:MM:SS to elaborate ON/OFF cycle used in Audiomoth.

We used Audiomoth v1.2.0 for all recordings.

The main settings are:
- Sampling rate: 250kHz (384kHz were used for our June recordings)
- Gain: medium
- Filter: none
- Amplitude threshold: none
- Recording ON/OFF cycle: 1795 sec ON and 5 sec OFF (total 1800 sec, or 30 mins for each recording file)
	- Example (cycle duration 30 mins):
		Cycle # | Recording ON | Recording OFF
		--------|--------------|--------------
		1 | 00:00:00-00:29:55 | 00:29:55-00:30:00
		2 | 00:30:00-00:59:55 | 00:59:55-01:00:00
		3 | 01:00:00-01:29:55 | 01:29:55-01:30:00
- Daily recording period: 00:00:00-24:00:00

