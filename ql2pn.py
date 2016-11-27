#!/usr/bin/env python3
# coding=utf-8

import argparse
import codecs
import os
from datetime import datetime
from time import mktime, strftime


def mkparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--logdir', '-l', type=str, default='', help='Path to Q2005a log directory.', required=True)
    parser.add_argument('--resdir', '-r', type=str, default='.', help='Path to output directory.', required=False)
    return parser


def getnumbers(logdir):
    ff = os.listdir(logdir)
    return ff


def getlogfiles(logdir, uids):
    result = []
    for uid in uids:
        flog = os.path.join(logdir, uid, 'History')
        for f in os.listdir(flog):
            result.append([os.path.join(flog, f), uid])
    return result


def reslogpath(resdir, uid):
    return os.path.join(resdir, 'icq', uid)


def frmtime(utime):
    ptime = datetime.fromtimestamp(utime).strftime('%Y-%m-%d.%H%M%S')
    return '%s%s.html' % (ptime, strftime('%z%Z'))


def date2unix(gtime):
    do = datetime.strptime(gtime, '%H:%M:%S %d/%m/%Y')
    return int(mktime(do.timetuple()))


def readlog(lfile):
    return codecs.open(lfile, 'r', encoding='cp1251', errors='ignore').read()


def genlogname(resdir, uid, utime):
    return os.path.join(reslogpath(resdir, uid), frmtime(utime))


def createhtml(resfile, recid, recdate, uid, contents):
    row = 'Conversation with %s at %s on %s (icq)' % (recid, recdate, uid)
    html = '<html><head><meta http-equiv="content-type" content="text/html; ' \
           'charset=UTF-8"><title>%s</title></head><body><h3>%s</h3>%s</body></html>' % (row, row, contents)

    with open(resfile, 'w') as tfile:
        tfile.write(html)


def parselog(lfile, resdir, uid):
    logfile = readlog(lfile)


def main():
    params = mkparser().parse_args()
    logdir = params.logdir
    for lfile in getlogfiles(logdir, getnumbers(logdir)):
        parselog(lfile[0], params.resdir, lfile[1])


if __name__ == '__main__':
    main()
