#!/bin/bash

function greibach() {
	in=$1;

	variables=($(echo $(cat "${in}") | \
		sed -e "s/ //g" -e 's/}$//' | \
		cut -f2 -d':' | \
		sed 's/^\[\[\([^]]*\).*$/\1/' | \
		tr -d "\"" | \
		tr "," " "));

	symbols=($(echo $(cat "${in}") | \
		sed -e "s/ //g" -e 's/}$//' | \
		cut -f2 -d':' | \
		sed 's/^\[\[[^]]*],\[\([^]]*\)\].*$/\1/' | \
		tr -d "\"" | \
		tr "," " "));

	rules=($(echo $(cat "${in}") | \
		sed -e "s/ //g" -e 's/}$//' | \
		cut -f2 -d':' | \
		sed 's/^\[\[[^]]*\],\[[^]]*\],\[\(.*\)\],.*$/\1,/' | \
		tr -d "\"" | \
		sed 's/\[\([^,]*\),\([^]]*\)\],/\1:\2 /g'));

	start=$(echo $(cat "${in}") | \
		sed -e "s/ //g" -e 's/}$//' | \
		cut -f2 -d':' | \
		sed 's/.*,\(.*\)]$/\1/' | \
		tr -d "\"");

	for r in ${rules[@]}; do
		lhs=${r/:*/};
 		rhs=${r/*:/};

		[[ " ${variables[*]} " =~ " ${lhs} " ]] || return 1

		if [ "${rhs}" == "#" ]; then
			[ "${lhs}" == "${start}" ] || return 1;
		else
			[[ " ${symbols[*]} " =~ " ${rhs:0:1} " ]] || return 1
			for ((i=1; i<${#rhs}; i++)); do
				[[ " ${variables[*]} " =~ " ${rhs:i:1} " ]] || return 1
			done
		fi
	done

	[[ " ${variables[*]} " =~ " ${start} " ]] || return 1

	return 0;
}

if [ $# -eq 0 ]; then
	echo "Usage: $0 [GNF]";
	exit 1;
fi

set -f

if greibach "${1}"; then
	echo 'Yes';
else
	echo 'No';
	exit 1;
fi
