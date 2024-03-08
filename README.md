### Description

This is a gdb pretty-printers for common types of userver-framework.
This is experimental feature to debug logical issues, use this code at your own risk.
Feel free to make an issue or pull-request.

How it looks when printing a `formats::json::Value` variable:
```(sh)
$1 = userver::v2_0_0_rc::formats::json::Value(version=0,data={"a":[1,{}],"b":[true,false],"c":{"internal":{"subkey":2}},"i":-1,"u":1,"i64":-1.8446744073709552e+19,"u64":18446744073709551614,"d":0.40000000000000002})
```


### Dependencies

Fedora: `sudo dnf debuginfo-install yaml-cpp-0.7.0-4.fc39.x86_64`


### Usage

At least you need pull [userver-framework](https://github.com/userver-framework/userver) and build
debug.

```(sh)
git clone --depth 1 https://github.com/userver-framework/userver
cd userver
mkdir build_debug && cd build_debug
cmake -DCMAKE_CXX_COMPILER=clang++-17 -DUSERVER_FEATURE_GRPC=OFF -DUSERVER_FEATURE_POSTGRESQL=OFF \
      -DUSERVER_FEATURE_MYSQL=OFF -DUSERVER_FEATURE_STACKTRACE=OFF -DUSERVER_FEATURE_CLICKHOUSE=OFF \
      -DUSERVER_USE_LD=lld ..
make
```

Now gdb needs to be configured regarding [Python Auto-Loading](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-Auto_002dloading.html#Python-Auto_002dloading) documentation for your executable or library. See objfile script `objfile-gdb.py` and `.debug_gdb_scripts` sections in [References](#References).
The way how to do it is left to the user's discretion.

Let's describe the steps required to enable pretty-printers using sample/json2yaml.

#### Usage sample

Simplified, we need to provide to gdb `scripts-directory` and `safe-path` where our executable file is placed, like this:
```
gdb \
    -iex "add-auto-load-scripts-directory samples/json2yaml" \
    -iex 'add-auto-load-safe-path samples/json2yaml' \
    ...
```

To make an experiment lets create `gdb-run.sh` with the following content:
```(sh)
#!/bin/bash

JSON_SAMPLE='r <<<"{\"a\":[1,{}],\"b\":[true,false],\"c\":{\"internal\":{\"subkey\":2}},\"i\":-1,\"u\":1,\"i64\":-18446744073709551614,\"u64\":18446744073709551614,\"d\":0.4}"'

# at userver root directory
cd build_debug && \
gdb \
    -iex "add-auto-load-scripts-directory samples/json2yaml" \
    -iex 'add-auto-load-safe-path samples/json2yaml' \
    -ex 'b json2yaml.cpp:53' \
    -ex $JSON_SAMPLE \
    -ex 'p json' \
    -ex 'fg' \
    -ex 'q' \
    --args samples/json2yaml/userver-samples-json2yaml
```

After run this script you will see something like:
```
$ bash ./gdb-run.sh
...
Breakpoint 1, main () at userver/samples/json2yaml/json2yaml.cpp:53
53        formats::yaml::Serialize(json.ConvertTo<formats::yaml::Value>(), std::cout);
$1 = {holder_ = {static kInvalidVersion = 18446744073709551615,
    data_ = std::shared_ptr<userver::v2_0_0_rc::formats::json::impl::VersionedValuePtr::Data> (use count 1, weak count 0) = {get() = 0x7ffff3e33010}},
  root_ptr_for_path_ = 0x7ffff3e33010, value_ptr_ = 0x7ffff3e33010, depth_ = 0, lazy_detached_path_ = {parent_value_ptr_ = 0x0, parent_depth_ = 0,
    virtual_path_ = Python Exception <class 'gdb.error'>: There is no member named _M_p.
}}
...
```
Looks like a mess and useless for debugging a logical issue.

Now prepare pretty-printers:
```(sh)
git clone https://github.com/theg4sh/userver-gdb-pp
export USERVER_GDB_PP_DIR="$(readlink -f userver-gdb-pp)"

(cd userver/build_debug/samples/json2yaml && \
  ln -s $USERVER_GDB_PP_DIR/userver_gdb_pp/__init__.py userver-samples-json2yaml-gdb.py)
```

and now check the result:
```(sh)
$ bash ./gdb-run.sh
...
Breakpoint 1, main () at /home/arkcoon/repos/theg4sh/userver/samples/json2yaml/json2yaml.cpp:53
53        formats::yaml::Serialize(json.ConvertTo<formats::yaml::Value>(), std::cout);
$1 = userver::v2_0_0_rc::formats::json::Value(version=0,data={"a":[1,{}],"b":[true,false],"c":{"internal":{"subkey":2}},"i":-1,"u":1,"i64":-1.8446744073709552e+19,"u64":18446744073709551614,"d":0.40000000000000002})
...
```
That's much better!


### References

- [GDB Python API Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-API.html#Python-API)
- [GDB Auto-load directories](https://sourceware.org/gdb/current/onlinedocs/gdb.html/objfile_002dgdbdotext-file.html#set-auto_002dload-scripts_002ddirectory)
- [The objfile-gdb.ext file](https://sourceware.org/gdb/current/onlinedocs/gdb.html/objfile_002dgdbdotext-file.html#set-auto_002dload-scripts_002ddirectory)
- [The .debug_gdb_scripts section](https://sourceware.org/gdb/current/onlinedocs/gdb.html/dotdebug_005fgdb_005fscripts-section.html#dotdebug_005fgdb_005fscripts-section)
