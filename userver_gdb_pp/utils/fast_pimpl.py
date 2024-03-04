import gdb

# @see (gdb) info types userver::v2_0_0_rc::utils::FastPimpl


class UtilsFastPimpl(gdb.ValuePrinter):
    "Print utils::FastPimpl<T>"

    def __init__(self, val):
        self.__val = val

    def to_string(self):
        storage = self.__val['storage_']
        storage_ptr = storage.cast(storage.type.pointer())

        underlying_type = self.__val.type.template_argument(0)
        underlying_data = storage_ptr.reinterpret_cast(
            underlying_type.pointer(),
        ).dereference()
        return f'{self.__val.type}(storage_={underlying_data})'

    def display_init(self):
        return 'utils::FastPimpl<T>'


def register_printers(pp_collection):
    pp_collection.add_printer(
        'utils::FastPimpl<T>',
        r'(^.*::|^)utils::FastPimpl<.*>$',
        UtilsFastPimpl,
    )
