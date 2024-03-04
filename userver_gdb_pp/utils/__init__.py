from userver_gdb_pp.utils import fast_pimpl

def register_printers(pp_collection):
    fast_pimpl.register_printers(pp_collection)
