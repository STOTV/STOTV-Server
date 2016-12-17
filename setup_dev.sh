#!/bin/sh
echo STOTV-Setup Script
echo Please verify that Python 3, PIP, and Bower is installed
read -p "Press enter to continue"
pip install -r requirements.txt
python testdata.py
cd static
bower install
read -p "Press enter to exit script"