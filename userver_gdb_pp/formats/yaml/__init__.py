from userver_gdb_pp.formats.yaml import value


def register_printers(pp_collection):
    value.register_printers(pp_collection)
