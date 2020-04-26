#!/usr/bin/env bash
find . -name "*.py" | xargs black --line-length 100
