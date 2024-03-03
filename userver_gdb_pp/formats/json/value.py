import gdb
import gdb.printing

from userver_gdb_pp.formats.json import rapidjson

class FormatsJsonValue(gdb.ValuePrinter):
    "Print formats::json::Value"

    def __init__(self, val):
        self.__val = val

    def to_string(self):
        versioned_data_ptr = self.__val['holder_']['data_']['_M_ptr']
        if versioned_data_ptr is None:
            return f'{self.__val.type}(kNone)'
        versioned_data = versioned_data_ptr.dereference()

        # native -> rapidjson
        native_data = versioned_data['native']['data_']

        data_type = rapidjson.rj_get_type(native_data['f']['flags'])
        version = versioned_data['version'].cast(
            gdb.lookup_type('unsigned long'),
        )
        data = data_type(
            versioned_data['native'],
            native_data['f']['flags'],
        )
        return (
            f'{self.__val.type}(version={version},'
            f'data={data.to_string()})'
        )

    def display_init(self):
        return 'formats::json::Value'

def formats_json_value_lookup_function():
    pp = gdb.printing.RegexpCollectionPrettyPrinter('userver')
    pp.add_printer(
        'formats::json::Value',
        r'(^.*::|^)formats::json::Value$',
        FormatsJsonValue,
    )
    return pp

def register_printers(objfile):
    gdb.printing.register_pretty_printer(
        objfile,
        formats_json_value_lookup_function(),
    )

