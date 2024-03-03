import sys
import os

import gdb

def register_printers(objfile):
    import userver_gdb_pp.formats as userver_formats
    userver_formats.register_printers(objfile)

if __name__ == '__main__':
    sys.path.insert(0, os.environ['USERVER_GDB_PP_DIR'])
    register_printers(gdb.current_objfile())
