#!/bin/sh
echo STOTV-Setup Script
echo Please verify that Python 3, and PIP is installed
read -p "Press enter to continue"
pip install -r requirements.txt
python addDevice.py
read -p "Press enter to exit script"