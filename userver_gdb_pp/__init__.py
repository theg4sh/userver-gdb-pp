import sys
import os

import gdb


def register_printers(objfile):
    import userver_gdb_pp.formats as userver_formats
    import userver_gdb_pp.utils as userver_utils

    pp = gdb.printing.RegexpCollectionPrettyPrinter('userver')
    userver_formats.register_printers(pp)
    userver_utils.register_printers(pp)

    gdb.printing.register_pretty_printer(objfile, pp)


if __name__ == '__main__':
    sys.path.insert(0, os.environ['USERVER_GDB_PP_DIR'])
    register_printers(gdb.current_objfile())
