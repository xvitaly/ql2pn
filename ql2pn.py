#!/usr/bin/env python
# coding=utf-8

import argparse


def mkparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--logdir', type=str, default='', help='Path to Q2005a log directory.', required=True)
    parser.add_argument('--resdir', type=str, default='', help='Path to output directory.', required=True)
    return parser


def main():
    n = mkparser().parse_args()


if __name__ == '__main__':
    main()