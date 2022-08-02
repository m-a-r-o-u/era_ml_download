#!/usr/bin/env python

'''
This script is meant to download era5 model level data
'''


import argparse
import cdsapi
import os
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from pandas.tseries.offsets import Day
import sys
import urllib3
import xarray as xr

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_era_ml(date, area, ofname):
    c = cdsapi.Client()

    product = 'reanalysis-era5-complete'

    specs = {}
    specs['class'] = 'ea'
    specs['date'] = date
    specs['expver'] = '1'
    specs['levelist'] = '124/to/137/by/1'
    specs['levtype'] = 'ml'
    specs['param']  = '129/130/131/132/133'
    specs['stream'] = 'oper'
    specs['time'] = '00/to/23/by/1'
    specs['type'] = 'an'
    specs['area'] = area # North, West, South, East
    specs['grid'] = '0.25/0.25'
    specs['format'] = 'netcdf'

    # print request
    print('*** request:')
    print(f'*** {product}')
    for k, v in specs.items():
        print(f'*** {k} {v}')
    print()

    c.retrieve(product, specs, ofname)


def get_days(start_date, end_date, binning='daily'):
    dates = []

    if binning == 'monthly':
        for beg in pd.date_range(start_date, end_date, freq='MS'):
            p = pd.Period(beg.strftime("%Y-%m-%d")).days_in_month
            start = beg.strftime("%Y-%m-%d")
            end = (beg + Day((p-1))).strftime("%Y-%m-%d")
            days = [_.strftime("%Y-%m-%d")  for _ in pd.date_range(start, end, freq='D')]
            dates.append(days)
    elif binning == 'daily':
        for day in pd.date_range(start_date, end_date, freq='D'):
            dates.append(day.strftime("%Y-%m-%d"))
    else:
        print(f'*** binning: {binning} not implemented')
    return dates


def arg_bool(x):
    if x in ['False', 'false', 'FALSE']:
        return False
    elif x in ['True', 'true', 'TRUE']:
        return True
    else:
        raise InputError(f'*** Unknown input: {x}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--area', help='North/West/South/East')
    parser.add_argument('--opath', help='Path to the output folder')
    parser.add_argument('--start_date')
    parser.add_argument('--end_date')
    parser.add_argument('--binning', default='daily')
    parser.add_argument('--test', type=arg_bool)
    args = parser.parse_args()

    # revere, therefore download the most recent first
    days = get_days(args.start_date, args.end_date, args.binning)[::-1]

    for sdays in days:
        date = f'{sdays[0]}/to/{sdays[-1]}'

        ofname = os.path.join(args.opath, date.replace('/', '_') + '.nc')
        if os.path.isfile(ofname):
            print(f'*** File exists, check integrety: {ofname}')
            continue

        download_era_ml(date, args.area, ofname)
        print(f'*** open {ofname}')

        if args.test:
            sys.exit()
