#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# http://code.google.com/p/soc/wiki/PythonStyleGuide

# Depends on RIL python lib (included), originally by Kosei Kitahara (https://bitbucket.org/Surgo/ril/)

# Note: Update test_configs.py with your valid credentials.

import optparse

import urllib2
from mechanize import Browser

import readitlater
import test_configs as configs

def main():
  # Command line options.
  parser = optparse.OptionParser('usage: %prog [options]')
  parser.add_option('--unread', dest='unread', action='store_true',
                    default=False, help='Only tag unread items')
  (opts, args) = parser.parse_args()

  # Get all items.
  api = readitlater.API(configs.RIL_APIKEY, configs.RIL_USERNAME,
                        configs.RIL_PASSWORD)
  items = api.get(state=('unread' if opts.unread else None))
  list = items['list']

  br = Browser()

  # Iterate over items.
  for k, v in list.items():
      #if v['title'] == v['url']:
      if not v['title']:
          print u'Found: {0} ({1})'.format(v['title'], v['url']);
          try:
              doc = br.open(v['url']);
          except urllib2.HTTPError, e:
              print u'Error fetching page: {0}'.format(e.code)
              continue

          if not br.viewing_html():
              print u'Not a HTML file!'
          else:
              title = br.title();
              print u'New title: {0}'.format(title.decode('ascii', 'ignore'))
              # Send the new tags to RIL.
              api.send(update_title=[{'url': v['url'], 'title': title}])


if __name__ == '__main__':
  main()
