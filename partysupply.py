#!/usr/bin/env python

import sys
from optparse import OptionParser

import partysupply

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", default=8080,
                  help="PORT to listing on, defaults to 8080", metavar="PORT")
parser.add_option("-t", "--tags", dest="tags", default="partysupply",
                  help="TAGS to follow, delimit multiple tags with commas", metavar="TAGS")

# python partysupply.py subscription add tag TAG

(options, args) = parser.parse_args()

partysupply.cli(args, options)
