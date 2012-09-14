#!/usr/bin/env python

import sys
from optparse import OptionParser

import partysupply

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", default=8080,
                  help="PORT to listing on, defaults to 8080", metavar="PORT")

# python partysupply.py subscription add tag TAG

(options, args) = parser.parse_args()

partysupply.cli(args, options)
