#!/usr/bin/env python
# coding=utf-8

import argparse
import os
from datetime import datetime
from time import mktime


def mkparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--logdir', type=str, default='', help='Path to Q2005a log directory.', required=True)
    parser.add_argument('--resdir', type=str, default='', help='Path to output directory.', required=True)
    return parser


def getnumbers(logdir):
    ff = os.listdir(logdir)
    return ff


def getlogfiles(logdir, ids):
    result = []
    for id in ids:
        flog = os.path.join(logdir, id, 'History')
        for xx in os.listdir(flog):
            result.append(os.path.join(flog, xx))
    return result


def gmt2unix(gtime):
    do = datetime.strptime(gtime, '%H:%M:%S %d/%m/%Y')
    return int(mktime(do.timetuple()))


def main():
    params = mkparser().parse_args()
    logdir = params.logdir
    logs = getlogfiles(logdir, getnumbers(logdir))

if __name__ == '__main__':
    main()
