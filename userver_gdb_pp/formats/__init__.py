import userver_gdb_pp.formats.json as formats_json

def register_printers(objfile):
    formats_json.register_printers(objfile)
