#!/usr/bin/python

import platform
import sys
import os
import argparse
import shotwelldb

supported = ['Linux']

def default_dir():
    directory = None
    if platform.system() in [ "Linux" ]:
        directory = "/".join([os.environ['HOME'], '.shotwell'])
    return directory

def database(dbdir): 
    dbfile = None
    if platform.system() in [ "Linux" ]:
        dbfile = "/".join([dbdir, 'data', 'photo.db'])
    return dbfile

def parse_arguments():
    parser = argparse.ArgumentParser(description='Tag Shotwell Photos.')
    parser.add_argument('--pattern', type=str, required=True,
                        help='a regular expression to match')
    parser.add_argument('--dbdir', type=str,
                        default=default_dir(),
                        help='Shotwell database directory')
    parser.add_argument('tags', metavar='tag', nargs='*', default=[],
                        help='List of tags')
    parser.add_argument('--event', type=str, required=False,
                        help='Set event name')
    return parser.parse_args()
    

def main():
    args = parse_arguments()
    db = shotwelldb.Library(database(args.dbdir))
    photos = db.photo_dir_match(args.pattern)

    if args.event:
        if db.event_exists(args.event) == False:
            db.create_event(args.event)
        eventid = db.get_event(args.event)
        for photo in photos:
            db.set_photo_eventid(photo, eventid)
    
    for tag in args.tags:
        if db.tag_exists(tag):
            db.tag_add_photoids(photos)
        else:
            db.add_tag(tag, photos)
            
if __name__ == "__main__":
    assert platform.system() in supported
    main()

