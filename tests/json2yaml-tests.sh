#!/bin/bash

#$PRETTY_PRINTER_LIST="-ex 'info pretty-printer'"
#$SHOW_SCRIPTS_DIRECTORY="-ex 'show auto-load scripts-directory'"
#$SHOW_AUTOLOAD_SAFEPATH="-ex 'show auto-load safe-path'"

JSON_SAMPLE='r <<<"{\"a\":[1,{}],\"b\":[true,false],\"c\":{\"internal\":{\"subkey\":2}},\"i\":-1,\"u\":1,\"i64\":-18446744073709551614,\"u64\":18446744073709551614,\"n\":null,\"d\":0.4}"'


function run_gdb() {
	gdb \
	  -iex 'add-auto-load-scripts-directory samples/json2yaml' \
	  -iex 'add-auto-load-safe-path samples/json2yaml' \
		$SHOW_AUTOLOAD_SAFEPATH \
	  $SHOW_SCRIPTS_DIRECTORY \
		$PRETTY_PRINTER_LIST \
		"${@}"
}

function test_formats_json_value() {
	run_gdb \
		-ex 'b json2yaml.cpp:53' \
		-ex "$JSON_SAMPLE" \
		-ex 'p json' \
		-ex 'fg' \
		-ex 'q' \
		--args samples/json2yaml/userver-samples-json2yaml
}

function test_formats_yaml_value() {
	run_gdb \
		-ex 'b json2yaml.cpp:53' \
		-ex "$JSON_SAMPLE" \
		-ex 's' \
		-ex 'p *this' \
		-ex 'fg' \
		-ex 'q' \
		--args samples/json2yaml/userver-samples-json2yaml
}

function test_utils_fast_pimpl() {

	run_gdb \
		-ex 'b userver::v2_0_0_rc::utils::FastPimpl<YAML::Node, 64ul, 8ul, false>::FastPimpl<YAML::Node const&>(YAML::Node const&)' \
		-ex "$JSON_SAMPLE" \
		-ex 'n' \
		-ex 'p *this' \
		-ex 'disable breakpoints' \
		-ex 'fg' \
		-ex 'q' \
		--args samples/json2yaml/userver-samples-json2yaml
}

test_formats_json_value
test_formats_yaml_value
test_utils_fast_pimpl

# for debugging move extra `-ex ... \` here
echo \
		> /dev/null

# vim: ts=2 sw=2 et
