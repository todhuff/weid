#!/bin/bash

CONFIG_DIR="/etc/weid"

	echo "Installing weid sample config files to ${CONFIG_DIR}"
if  [ ! -e "${CONFIG_DIR}" ]; then
	echo "mkdir ${CONFIG_DIR}"
	mkdir ${CONFIG_DIR}
fi
cp -n ./config/* ${CONFIG_DIR}
