#!/bin/bash

# Provide SSH connectivity to internal hosts. Also, take care to filter SSH break-in attempts 
# to those internal hosts

{%- set forwarded_ports = [] %}

{% for host in groups["internal"] -%}
{%- set from_host = hostvars[host].networking.nat.ssh.external_host| default('') -%}
{%- set from_port = hostvars[host].networking.nat.ssh.external_port| int(default=0) -%}
{%- if (from_host == inventory_hostname) and (from_port > 0) and not (from_port in forwarded_ports) %}
{%- set to_addr = hostvars[host].networking.if.internal_ipv4.address -%}
{%- do forwarded_ports.append(from_port) %} 
# Forward traffic to port {{from_port}} to host {{host}} 
iptables -t nat -i ${public_ip4_iface} -A PREROUTING -j DNAT -p tcp -d ${public_ip4} --dport '{{from_port}}' --to-destination '{{to_addr}}:22'
# Filter forwarded traffic to {{from_port}} for host {{host}}
iptables -A FORWARD -i ${public_ip4_iface} -p tcp -m tcp \
  --dport '{{from_port}}' -m state --state NEW -m recent --set --name 'SSH_FWD_{{from_port}}' --rsource 
iptables -A FORWARD -i ${public_ip4_iface} -p tcp -m tcp \
  --dport '{{from_port}}' -m state --state NEW -m recent --update --seconds 60 --hitcount 8 --name 'SSH_FWD_{{from_port}}' --rsource -j REJECT
{% endif %}

{% endfor %}
