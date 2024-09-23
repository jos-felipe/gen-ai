#!/bin/zsh

find . -type f -name "*.sh" | sed 's/\.sh$//'
