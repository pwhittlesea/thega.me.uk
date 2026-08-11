---
title: "A Simple Script Base"
date: 2024-03-30 21:23:00 +0000
last_modified_at: 2024-10-21 20:30:48 +0000
categories: [code]
tags: [bash]
---

Sometimes you just need a script that takes arguments.
This is a simple script which will call different functions based on the first argument from the user.

<!--more-->

```bash
#!/usr/bin/env bash

set +e
#set -x # print all executed commands to the terminal

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function _red {
    echo -e "\e[1;31m${1}\e[0m"
}

function _one {
    echo "One stuff"
}

function _two {
    echo "Two jazz"
}

function _help() {
    echo "Usage: ${SCRIPT_DIR}/example.sh <option>"
    echo
    echo "Options:"
    echo "    one - The first thing"
    echo "    two - A second thing"
}

if test "$#" -lt 1; then
    _red "Illegal number of parameters"
    exit 1
fi

case "${1}" in
    'one') _one ;;
    'two') _two ;;
    *) _help
       exit 1
       ;;
esac
exit 0
```
