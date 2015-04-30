#!/bin/bash

iptables -t nat -A POSTROUTING -o ${public_ip4_iface} --source ${internal_ip4_network} -j MASQUERADE
