from userver_gdb_pp.formats.json import value

def register_printers(objfile):
    value.register_printers(objfile)

