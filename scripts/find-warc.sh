#!/usr/bin/env bash
 while read -r urim
 do
 read item warc <<<$(curl -Is “$urim” | grep -iPo “^x-archive-src: \K\S+” | sed ‘s|/| |’)
 cols=$(ia metadata “$item” | jq -r ‘.metadata.collection | join(“,”)’)
 echo -e “$urimt\t$colst\t$itemt\t$warc”
 done < <(cat “$@“)