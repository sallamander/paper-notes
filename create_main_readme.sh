#!/bin/bash

rm README.md
python create_main_readme.py
doctoc README.md
