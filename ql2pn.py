#!/usr/bin/env python
# coding=utf-8

import argparse, os, glob


def mkparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--logdir', type=str, default='', help='Path to Q2005a log directory.', required=True)
    parser.add_argument('--resdir', type=str, default='', help='Path to output directory.', required=True)
    return parser


def getnumbers(logdir):
    ff = os.listdir(logdir)
    return ff


def main():
    n = mkparser().parse_args()

if __name__ == '__main__':
    main()