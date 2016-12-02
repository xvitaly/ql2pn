#!/usr/bin/env python3
# coding=utf-8

#
# Q2005a to Pidgin log converter
# Copyright (c) 2016 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import codecs
import html
import os
import re
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


def convtime(utime):
    return datetime.fromtimestamp(utime).strftime('%d.%m.%Y %H:%M:%S')


def msgtime(utime):
    return datetime.fromtimestamp(utime).strftime('(%H:%M:%S)')


def date2unix(gtime):
    do = datetime.strptime(gtime, '%H:%M:%S %d/%m/%Y')
    return int(mktime(do.timetuple()))


def readlog(lfile):
    return codecs.open(lfile, 'r', encoding='cp1251', errors='ignore').read()


def genlogname(resdir, uid, utime):
    return os.path.join(reslogpath(resdir, uid), frmtime(utime))


def createhtml(resfile, recid, recdate, uid, contents):
    # Checking directory exists...
    resdir = os.path.dirname(resfile)
    if not os.path.exists(resdir):
        os.makedirs(resdir)

    # Generating HTML file...
    row = 'Conversation with %s at %s on %s (icq)' % (recid, convtime(recdate), uid)
    rhtml = '<html><head><meta http-equiv="content-type" content="text/html; ' \
            'charset=UTF-8"><title>%s</title></head><body><h3>%s</h3>%s\n</body></html>' % (row, row, contents)

    # Writing result to text file...
    with open(resfile, 'w') as tfile:
        tfile.write(rhtml)


def parserow(row):
    # Find index of date in row...
    ri = row.rindex('(')

    # Return result...
    return [row[:ri-1], date2unix(row[ri+1:-1])]


def formatmsg(msg):
    urlfn = re.compile('(https?:\/\/\S+)')
    return urlfn.sub(r'<a href="\1">\1</a>', html.escape(msg))


def formatline(utype, udate, uname, umsg):
    hcolor = '#16569E' if utype == '>-' else '#A82F2F'
    return '<font color="%s"><font size="2">%s</font> <b>%s:</b></font> %s<br/>\n' % (
        hcolor, msgtime(udate), uname, formatmsg(umsg))


def parselog(lfile, resdir, uid):
    # Reading log file...
    logfile = readlog(lfile)

    # Setting variables...
    recid = os.path.splitext(os.path.basename(lfile))[0]
    resmsg = ''
    ipx = 0
    wrx = 1
    firstdate = 0
    lastdate = 0

    # Parsing contents of log file...
    for lln in logfile.split('--------------------------------------'):
        # Parsing sent or received message...
        ln = lln.splitlines(keepends=False)

        # Checking for message in parsed list...
        if len(ln) >= 3:
            # Parsing first row with nickname and date...
            fr = parserow(ln[1])

            # Checking if message belongs to current conversation or not...
            ax = fr[1] - lastdate

            # Saving last message's time...
            lastdate = fr[1]

            # Extracting whole conversation (for 12 hours)...
            if (ax < 43200) or (ipx == 0):
                # Extracting date of conversation start...
                if ipx == 0:
                    firstdate = fr[1]

                # Increment counters...
                ipx += 1
                wrx = 1

                # Writing conversation to special variable...
                resmsg += formatline(ln[0], fr[1], fr[0], ln[2])
            else:
                # Conversation extracted. Writing to file...
                createhtml(os.path.join(resdir, 'icq', uid, recid, frmtime(firstdate)), recid, firstdate, uid, resmsg)

                # Nulling variables...
                ipx = 0
                wrx = 0

                # Saving row to a new conversation...
                resmsg = formatline(ln[0], fr[1], fr[0], ln[2])

    # Writing last conversation to file too...
    if wrx != 0:
        createhtml(os.path.join(resdir, 'icq', uid, recid, frmtime(firstdate)), recid, firstdate, uid, resmsg)

def main():
    # Receiving parameters...
    params = mkparser().parse_args()

    # Generating list of files and starting parsing them...
    for lfile in getlogfiles(params.logdir, getnumbers(params.logdir)):
        try:
            # Print message with current filename to console...
            print('Parsing file "%s"...' % lfile[0])

            # Starting parser...
            parselog(lfile[0], params.resdir, lfile[1])
        except Exception as ex:
            # Show error message on exception...
            print('An error occurred "%s" while parsing "%s" file.' % (ex.message, lfile[0]))


if __name__ == '__main__':
    main()
