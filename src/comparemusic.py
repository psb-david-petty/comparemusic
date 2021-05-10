#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# comparemusic.py
#
"""
comparemusic.py is...
"""

__author__ = "David C. Petty"
__copyright__ = "Copyright 2021, David C. Petty"
__license__ = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
__version__ = "0.0.1"
__maintainer__ = "David C. Petty"
__email__ = "david_petty@psbma.org"
__status__ = "Hack"

import argparse, os, sys


def files(path, verbose=False):
    """Return set of files in path."""
    assert os.path.isdir(path), f"'{path}' is not a directory"
    file_set = set()
    for dir_path, subdir_list, file_list in os.walk(path):
        dir_name = dir_path.replace(os.path.dirname(path + '/') + '/', '')
        subdir_list.sort()
        if verbose:
            print(f"Found directory: {dir_name}")
        for name in [os.path.join(dir_name, n) for n in file_list
                     if n != '.DS_Store']:
            if verbose:\
                print(f"\t{name}")
            file_set.add(name)
    return file_set


def compare(from_path, to_path,
        check_both=False, files_and_dirs=False, full_path=False, verbose=False):
    """Show differences between files in from_path and to_path."""
    print(f"* In '{from_path}' but not in '{to_path}'")

    # Collect from_path walk and to_path walk.
    from_files = files(from_path, verbose)
    to_files = files(to_path, verbose)

    difference = {os.path.dirname(name) if not files_and_dirs else name
                  for name in from_files - to_files}
    for name in sorted(difference):
        path = os.path.join(from_path, name) if full_path else name
        print(f"  '{path}'")

    # Only check both if check_both.
    if check_both:
        print(f"* In '{to_path}' but not in '{from_path}'")
        difference = {os.path.dirname(name) if not files_and_dirs else name
                      for name in to_files - from_files}
        for name in sorted(difference):
            path = os.path.join(to_path, name) if full_path else name
            print(f"  '{path}'")


class Parser(argparse.ArgumentParser):
    """Create OptionParser to parse command-line options."""
    def __init__(self, **kargs):
        argparse.ArgumentParser.__init__(self, **kargs)
        # self.remove_argument("-h")
        self.add_argument("-?", "--help", action="help",
                          help="show this help message and exit")
        self.add_argument('--version', action='version',
                          version=f"%(prog)s {__version__}")

    def error(self, msg):
        sys.stderr.write("%s: error: %s\n\n" % (self.prog, msg, ))
        self.print_help()
        sys.exit(2)


def main(argv):
    """This is a template that includes OptionParser-style arguments."""
    description = """Read two paths and compare the files."""
    formatter = lambda prog: \
        argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=30)
    parser = Parser(description=description, add_help=False,
                    formatter_class=formatter)
    arguments = [
        # c1, c2, action, dest, default, help
        ('-b', '--both', 'store_true', 'BOTH', False,
         'calculate both FROM - TO and TO - FROM', ),
        ('-f', '--files', 'store_true', 'FILES', False,
         'include all files', ),
        ('-p', '--path', 'store_true', 'PATH', False,
         'include full path', ),
        ('-v', '--verbose', 'store_true', 'VERBOSE', False,
         'echo status information',),
    ]
    # Add optional arguments with values.
    for c1, c2, a, v, d, h in arguments:
        parser.add_argument(c1, c2, action=a, dest=v, default=d, help=h,)
    # Add positional arguments. 'NAME' is both the string and the variable.
    parser.add_argument("FROM", help="from folder")
    parser.add_argument("TO", help="to folder")
    # Parse arguments.
    pa = parser.parse_args(args=argv[1: ])
    if pa.VERBOSE:
        if pa.FROM:
            print(f"FROM    = '{pa.FROM}'")
        if pa.TO:
            print(f"TO      = '{pa.TO}'")
        print(f"BOTH    = {pa.BOTH}")
        print(f"FILES   = {pa.FILES}")
        print(f"PATH    = {pa.PATH}")
        print(f"VERBOSE = {pa.VERBOSE}")

    compare(pa.FROM, pa.TO, pa.BOTH, pa.FILES, pa.PATH, pa.VERBOSE)


if __name__ == '__main__':
    is_idle, is_pycharm, is_jupyter = (
        'idlelib' in sys.modules,
        int(os.getenv('PYCHARM', 0)),
        '__file__' not in globals()
    )
    if any((is_idle, is_pycharm, is_jupyter,)):
        # main(['parsereport.py', '/Volumes/Toshiba4T/music/COMPARE WITH MUSIC/',
        #       '/Volumes/Toshiba4T/music/Music/', ])
        main(['parsereport.py', '/Volumes/Toshiba4T/music/Music-DELETE/',
              '/Volumes/Toshiba4T/music/Music/', '-b', ])
    else:
        main(sys.argv)
