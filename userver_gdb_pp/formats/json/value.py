import gdb
import gdb.printing

from userver_gdb_pp.formats.json import rapidjson

class FormatsJsonValue(gdb.ValuePrinter):
    "Print formats::json::Value"

    def __init__(self, val):
        self.__val = val

    def to_string(self):
        if self.__val['value_ptr_'] is None:
            return f'{self.__val.type}(value_ptr_=nullptr)'

        value = self.__val['value_ptr_']
        native_data = value['data_'] # rapidjson

        data_type = rapidjson.rj_get_type(native_data['f']['flags'])
        data = data_type(value, native_data['f']['flags'])
        return f'{self.__val.type}(data={data.to_string()})'

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

