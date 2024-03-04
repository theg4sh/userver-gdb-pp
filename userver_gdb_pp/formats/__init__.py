import userver_gdb_pp.formats.json as formats_json


def register_printers(pp_collection):
    formats_json.register_printers(pp_collection)
