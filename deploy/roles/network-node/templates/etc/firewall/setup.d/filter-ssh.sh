#!/bin/bash

#
# Generated from Ansible for host {{inventory_hostname}} 
#

# Filter successive SSH attempts

if [ -n "${public_ip4_iface}" ]; then
    iptables -A INPUT -i ${public_ip4_iface} -p tcp -m tcp \
      --dport 22 -m state --state NEW -m recent --set --name SSH --rsource 
    iptables -A INPUT -i ${public_ip4_iface} -p tcp -m tcp \
      --dport 22 -m state --state NEW -m recent --update --seconds 40 --hitcount 8 --name SSH --rsource -j REJECT
fi

if [ -n "${internal_ip4_iface}" ]; then
    iptables -A INPUT -i ${internal_ip4_iface} -p tcp -m tcp \
      --dport 22 -m state --state NEW -m recent --set --name SSH_INT --rsource 
    iptables -A INPUT -i ${internal_ip4_iface} -p tcp -m tcp \
      --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 8 --name SSH_INT --rsource -j REJECT
fi

if [ -n "${public_ip6_iface}" ]; then
    ip6tables -A INPUT -i ${public_ip6_iface} -p tcp -m tcp \
      --dport 22 -m state --state NEW -m recent --set --name SSH --rsource 
    ip6tables -A INPUT -i ${public_ip6_iface} -p tcp -m tcp \
      --dport 22 -m state --state NEW -m recent --update --seconds 40 --hitcount 8 --name SSH --rsource -j REJECT
fi

