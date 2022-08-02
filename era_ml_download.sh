#!/bin/bash

# this is the shell wrapper script to download era5 model level data
# options you want to set:
#     opath - the output folder
#     south, north, west, east - the domain boarders
#     start_date and end_date
#     binning - possible values: monthly - downloads one file per month
#                                daily - downloads each day into a seperate file
#         daily needs more requests then monthly.

opath=./data/era_ml/
mkdir -p $opath

test=false

south=52.85
north=56.11
west=3.76
east=9.53
area="$north/$west/$south/$east"

start_date=2010-01-01
end_date=2021-12-31
binning='monthly'

bin=./src/era_ml_download.py
$bin --area $area --opath $opath --start_date $start_date --end_date $end_date --binning $binning --test $test
